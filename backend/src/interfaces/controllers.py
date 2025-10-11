from fastapi import APIRouter, HTTPException, Depends
from ..application.use_cases import PredictRiskUseCase, GenerateClinicalCaseUseCase, AnalyzeVariableImpactUseCase
from ..domain.entities import PatientData
from .dtos import (
    PatientDataRequest, RiskPredictionResponse, ClinicalCaseResponse,
    StudyRequest, StudyResponse, CaseAnswerRequest, CaseAnswerResponse
)

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