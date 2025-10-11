from pydantic import BaseModel, Field
from typing import Dict, Optional
from enum import Enum

class RiskLevelResponse(str, Enum):
    LOW = "baixo"
    MEDIUM = "medio"
    HIGH = "alto"

class PatientDataRequest(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Idade em anos")
    gender: int = Field(..., ge=1, le=2, description="Gênero (1: feminino, 2: masculino)")
    height: float = Field(..., ge=100, le=250, description="Altura em cm")
    weight: float = Field(..., ge=30, le=200, description="Peso em kg")
    ap_hi: int = Field(..., ge=70, le=300, description="Pressão arterial sistólica")
    ap_lo: int = Field(..., ge=40, le=200, description="Pressão arterial diastólica")
    cholesterol: int = Field(..., ge=1, le=3, description="Colesterol (1: normal, 2: alto, 3: muito alto)")
    gluc: int = Field(..., ge=1, le=3, description="Glicose (1: normal, 2: alto, 3: muito alto)")
    smoke: int = Field(..., ge=0, le=1, description="Fumante (0: não, 1: sim)")
    alco: int = Field(..., ge=0, le=1, description="Álcool (0: não, 1: sim)")
    active: int = Field(..., ge=0, le=1, description="Atividade física (0: não, 1: sim)")

class RiskPredictionResponse(BaseModel):
    risk_level: RiskLevelResponse
    probability: float
    confidence: float
    factors: Dict[str, str]
    ai_explanation: Optional[str] = None

class ClinicalCaseResponse(BaseModel):
    id: str
    patient_data: PatientDataRequest
    description: str
    created_at: str

class StudyRequest(BaseModel):
    patient_data: PatientDataRequest
    variable: str
    new_value: float

class StudyResponse(BaseModel):
    variable: str
    impact: float
    new_risk: RiskLevelResponse
    explanation: str

class CaseAnswerRequest(BaseModel):
    case_id: str
    predicted_risk: RiskLevelResponse

class CaseAnswerResponse(BaseModel):
    correct: bool
    correct_risk: RiskLevelResponse
    explanation: str