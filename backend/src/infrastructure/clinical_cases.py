import random
import uuid
from datetime import datetime
from typing import Optional
from ..domain.entities import ClinicalCase, PatientData, RiskLevel
from ..interfaces.repositories import ClinicalCaseRepository

class InMemoryClinicalCaseRepository(ClinicalCaseRepository):
    def __init__(self):
        self.cases = {}
        self.case_templates = [
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
            },
            {
                'description': 'Paciente feminina, 38 anos, sedentária, com sobrepeso',
                'data': {'age': 38, 'gender': 1, 'height': 165, 'weight': 85, 'active': 0, 'cholesterol': 2},
                'risk': RiskLevel.MEDIUM
            },
            {
                'description': 'Paciente masculino, 72 anos, ex-fumante, com pressão controlada',
                'data': {'age': 72, 'gender': 2, 'ap_hi': 130, 'ap_lo': 80, 'smoke': 0, 'alco': 0},
                'risk': RiskLevel.HIGH
            }
        ]
    
    async def generate_random_case(self) -> ClinicalCase:
        template = random.choice(self.case_templates)
        case_id = str(uuid.uuid4())
        
        # Gerar dados aleatórios baseados no template
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
        return self.cases.get(case_id)
    
    async def save_case(self, case: ClinicalCase) -> None:
        self.cases[case.id] = case