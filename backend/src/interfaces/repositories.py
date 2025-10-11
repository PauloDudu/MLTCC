from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.entities import ClinicalCase, PatientData, RiskPrediction

class MLModelRepository(ABC):
    @abstractmethod
    async def predict_risk(self, patient_data: PatientData) -> RiskPrediction:
        pass
    
    @abstractmethod
    async def analyze_variable_impact(self, patient_data: PatientData, variable: str, new_value: float) -> dict:
        pass

class ClinicalCaseRepository(ABC):
    @abstractmethod
    async def generate_random_case(self) -> ClinicalCase:
        pass
    
    @abstractmethod
    async def get_case_by_id(self, case_id: str) -> Optional[ClinicalCase]:
        pass
    
    @abstractmethod
    async def save_case(self, case: ClinicalCase) -> None:
        pass