from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import uuid
from ..domain.entities import ClinicalCase, PatientData, RiskLevel
from ..interfaces.repositories import ClinicalCaseRepository
from .database import ClinicalCaseModel, PredictionLogModel, get_db

class PostgresClinicalCaseRepository(ClinicalCaseRepository):
    def __init__(self, db: Session):
        self.db = db
    
    async def generate_random_case(self) -> ClinicalCase:
        import random
        
        case_templates = [
            {
                'description': 'Paciente masculino, 65 anos, com histórico de hipertensão e colesterol alto',
                'data': {'age': 65, 'gender': 2, 'ap_hi': 150, 'ap_lo': 95, 'cholesterol': 3, 'smoke': 0},
                'risk': RiskLevel.HIGH
            },
            {
                'description': 'Paciente feminina, 45 anos, atleta, sem comorbidades',
                'data': {'age': 45, 'gender': 1, 'ap_hi': 110, 'ap_lo': 70, 'cholesterol': 1, 'active': 1},
                'risk': RiskLevel.LOW
            },
            {
                'description': 'Paciente masculino, 55 anos, diabético, fumante',
                'data': {'age': 55, 'gender': 2, 'ap_hi': 140, 'ap_lo': 90, 'cholesterol': 2, 'gluc': 3, 'smoke': 1},
                'risk': RiskLevel.MEDIUM
            }
        ]
        
        template = random.choice(case_templates)
        case_id = str(uuid.uuid4())
        
        patient_data = PatientData(
            age=template['data'].get('age', random.randint(30, 80)),
            gender=template['data'].get('gender', random.randint(1, 2)),
            height=template['data'].get('height', random.randint(150, 190)),
            weight=template['data'].get('weight', random.randint(50, 100)),
            ap_hi=template['data'].get('ap_hi', random.randint(90, 180)),
            ap_lo=template['data'].get('ap_lo', random.randint(60, 120)),
            cholesterol=template['data'].get('cholesterol', random.randint(1, 3)),
            gluc=template['data'].get('gluc', random.randint(1, 3)),
            smoke=template['data'].get('smoke', random.randint(0, 1)),
            alco=template['data'].get('alco', random.randint(0, 1)),
            active=template['data'].get('active', random.randint(0, 1))
        )
        
        case = ClinicalCase(
            id=case_id,
            patient_data=patient_data,
            correct_risk=template['risk'],
            description=template['description'],
            created_at=datetime.now()
        )
        
        await self.save_case(case)
        return case
    
    async def get_case_by_id(self, case_id: str) -> Optional[ClinicalCase]:
        db_case = self.db.query(ClinicalCaseModel).filter(ClinicalCaseModel.id == case_id).first()
        if not db_case:
            return None
            
        patient_data = PatientData(
            age=db_case.age,
            gender=db_case.gender,
            height=db_case.height,
            weight=db_case.weight,
            ap_hi=db_case.ap_hi,
            ap_lo=db_case.ap_lo,
            cholesterol=db_case.cholesterol,
            gluc=db_case.gluc,
            smoke=db_case.smoke,
            alco=db_case.alco,
            active=db_case.active
        )
        
        return ClinicalCase(
            id=str(db_case.id),
            patient_data=patient_data,
            correct_risk=RiskLevel(db_case.correct_risk),
            description=db_case.description,
            created_at=db_case.created_at
        )
    
    async def save_case(self, case: ClinicalCase) -> None:
        db_case = ClinicalCaseModel(
            id=case.id,
            description=case.description,
            age=case.patient_data.age,
            gender=case.patient_data.gender,
            height=case.patient_data.height,
            weight=case.patient_data.weight,
            ap_hi=case.patient_data.ap_hi,
            ap_lo=case.patient_data.ap_lo,
            cholesterol=case.patient_data.cholesterol,
            gluc=case.patient_data.gluc,
            smoke=case.patient_data.smoke,
            alco=case.patient_data.alco,
            active=case.patient_data.active,
            correct_risk=case.correct_risk.value,
            created_at=case.created_at
        )
        
        self.db.add(db_case)
        self.db.commit()
        self.db.refresh(db_case)

def log_prediction(db: Session, patient_data: PatientData, risk_level: RiskLevel, probability: float, confidence: float):
    """Log da predição no banco"""
    log = PredictionLogModel(
        age=patient_data.age,
        gender=patient_data.gender,
        height=patient_data.height,
        weight=patient_data.weight,
        ap_hi=patient_data.ap_hi,
        ap_lo=patient_data.ap_lo,
        cholesterol=patient_data.cholesterol,
        gluc=patient_data.gluc,
        smoke=patient_data.smoke,
        alco=patient_data.alco,
        active=patient_data.active,
        predicted_risk=risk_level.value,
        probability=probability,
        confidence=confidence,
        created_at=datetime.now()
    )
    
    db.add(log)
    db.commit()
    db.refresh(log)