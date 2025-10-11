from typing import List
from ..domain.entities import PatientData, RiskPrediction, ClinicalCase, StudyResult
from ..interfaces.repositories import MLModelRepository, ClinicalCaseRepository
from ..infrastructure.ai_explainer import AIExplainer

class PredictRiskUseCase:
    def __init__(self, ml_repository: MLModelRepository):
        self.ml_repository = ml_repository
        self.ai_explainer = AIExplainer()
    
    async def execute(self, patient_data: PatientData) -> RiskPrediction:
        prediction = await self.ml_repository.predict_risk(patient_data)
        
        # Gerar explicação com IA
        try:
            patient_dict = {
                'age': patient_data.age,
                'ap_hi': patient_data.ap_hi,
                'ap_lo': patient_data.ap_lo,
                'cholesterol': patient_data.cholesterol,
                'weight': patient_data.weight,
                'height': patient_data.height,
                'smoke': patient_data.smoke,
                'active': patient_data.active
            }
            ai_explanation = self.ai_explainer.generate_explanation(
                patient_dict,
                prediction.risk_level.value,
                prediction.probability,
                prediction.factors
            )
            prediction.ai_explanation = ai_explanation
        except Exception as e:
            print(f"Erro ao gerar explicação: {e}")
            prediction.ai_explanation = "Explicação não disponível"
        
        return prediction

class GenerateClinicalCaseUseCase:
    def __init__(self, case_repository: ClinicalCaseRepository):
        self.case_repository = case_repository
    
    async def execute(self) -> ClinicalCase:
        return await self.case_repository.generate_random_case()

class AnalyzeVariableImpactUseCase:
    def __init__(self, ml_repository: MLModelRepository):
        self.ml_repository = ml_repository
    
    async def execute(self, patient_data: PatientData, variable: str, new_value: float) -> StudyResult:
        result = await self.ml_repository.analyze_variable_impact(patient_data, variable, new_value)
        
        return StudyResult(
            variable=variable,
            impact=result['impact'],
            new_risk=result['new_risk'],
            explanation=result['explanation']
        )