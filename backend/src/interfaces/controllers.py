from fastapi import APIRouter, HTTPException, Depends, Header
from ..application.use_cases import PredictRiskUseCase, GenerateClinicalCaseUseCase, AnalyzeVariableImpactUseCase
from ..domain.entities import PatientData
from ..infrastructure.auth import AuthService
from ..infrastructure.postgres_user_repository import PostgresUserRepository
from .dtos import (
    PatientDataRequest, RiskPredictionResponse, ClinicalCaseResponse,
    StudyRequest, StudyResponse, CaseAnswerRequest, CaseAnswerResponse
)
from typing import Optional

class CardiovascularController:
    def __init__(
        self,
        predict_use_case: PredictRiskUseCase,
        case_use_case: GenerateClinicalCaseUseCase,
        study_use_case: AnalyzeVariableImpactUseCase
    ):
        self.predict_use_case = predict_use_case
        self.case_use_case = case_use_case
        self.study_use_case = study_use_case
        self.user_repository = PostgresUserRepository()
        self.auth_service = AuthService()
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        @self.router.post("/predict", response_model=RiskPredictionResponse)
        async def predict_risk(request: PatientDataRequest):
            try:
                patient_data = PatientData(**request.model_dump())
                prediction = await self.predict_use_case.execute(patient_data)
                
                return RiskPredictionResponse(
                    risk_level=prediction.risk_level.value,
                    probability=prediction.probability,
                    confidence=prediction.confidence,
                    factors=prediction.factors,
                    ai_explanation=prediction.ai_explanation
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Dados inválidos: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/case", response_model=ClinicalCaseResponse)
        async def generate_case():
            try:
                case = await self.case_use_case.execute()
                
                return ClinicalCaseResponse(
                    id=case.id,
                    patient_data=PatientDataRequest(**case.patient_data.__dict__),
                    description=case.description,
                    created_at=case.created_at.isoformat()
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/study", response_model=StudyResponse)
        async def analyze_impact(request: StudyRequest):
            try:
                patient_data = PatientData(**request.patient_data.model_dump())
                result = await self.study_use_case.execute(
                    patient_data, request.variable, request.new_value
                )
                
                return StudyResponse(
                    variable=result.variable,
                    impact=result.impact,
                    new_risk=result.new_risk.value,
                    explanation=result.explanation
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/chat")
        async def chat_with_ai(request: dict):
            try:
                from ..infrastructure.ai_chat import AIChat
                chat = AIChat()
                response = chat.chat(
                    request['message'],
                    request['patient_data'],
                    request['prediction'],
                    request.get('chat_history', [])
                )
                return {"response": response}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/register")
        async def register(request: dict):
            try:
                senha_hash = self.auth_service.hash_password(request["senha"])
                user = self.user_repository.create_user(request["login"], request["nome"], senha_hash)
                if not user:
                    raise HTTPException(status_code=400, detail="Login já existe")
                return {"message": "Usuário criado com sucesso"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/login")
        async def login(request: dict):
            try:
                from datetime import datetime, timedelta
                user = self.user_repository.get_user_by_login(request["login"])
                if not user or not self.auth_service.verify_password(request["senha"], user.senha_hash):
                    raise HTTPException(status_code=401, detail="Credenciais inválidas")
                
                token = self.auth_service.create_token(user.id, user.login)
                expires_at = datetime.utcnow() + timedelta(hours=4)
                self.user_repository.save_token(user.id, token, expires_at)
                return {"token": token, "user": {"id": user.id, "login": user.login, "nome": user.nome}}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/save-caso")
        async def save_caso_resultado(request: dict, authorization: Optional[str] = Header(None)):
            try:
                current_user = self.get_current_user(authorization)
                acertou = request["gabarito"].lower() == request["resposta"].lower()
                self.user_repository.save_caso_historico(
                    current_user["user_id"], request["caso_dados"], request["gabarito"], request["resposta"], acertou
                )
                return {"message": "Resultado salvo", "acertou": acertou}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/historico")
        async def get_historico(authorization: Optional[str] = Header(None)):
            try:
                current_user = self.get_current_user(authorization)
                historico = self.user_repository.get_historico_user(current_user["user_id"])
                return {"historico": historico}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.delete("/delete-account")
        async def delete_account(authorization: Optional[str] = Header(None)):
            try:
                current_user = self.get_current_user(authorization)
                self.user_repository.delete_user(current_user["user_id"])
                return {"message": "Conta apagada com sucesso"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def get_current_user(self, authorization: Optional[str] = Header(None)):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token não fornecido")
        
        token = authorization.split(" ")[1]
        user = self.user_repository.verify_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        
        return {"user_id": user.id, "login": user.login}