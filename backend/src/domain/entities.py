from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime

class RiskLevel(Enum):
    LOW = "baixo"
    MEDIUM = "medio"
    HIGH = "alto"

@dataclass
class PatientData:
    age: int  # idade em anos
    gender: int  # 1: feminino, 2: masculino
    height: float  # altura em cm
    weight: float  # peso em kg
    ap_hi: int  # pressão arterial sistólica
    ap_lo: int  # pressão arterial diastólica
    cholesterol: int  # 1: normal, 2: acima do normal, 3: muito acima
    gluc: int  # 1: normal, 2: acima do normal, 3: muito acima
    smoke: int  # 0: não fuma, 1: fuma
    alco: int  # 0: não bebe, 1: bebe
    active: int  # 0: sedentário, 1: ativo

@dataclass
class RiskPrediction:
    risk_level: RiskLevel
    probability: float
    confidence: float
    factors: dict
    ai_explanation: Optional[str] = None

@dataclass
class ClinicalCase:
    id: str
    patient_data: PatientData
    correct_risk: RiskLevel
    description: str
    created_at: datetime

@dataclass
class StudyResult:
    variable: str
    impact: float
    new_risk: RiskLevel
    explanation: str