import joblib
import numpy as np
import pandas as pd
from typing import Dict
from ..domain.entities import PatientData, RiskPrediction, RiskLevel
from ..interfaces.repositories import MLModelRepository

class ScikitLearnMLRepository(MLModelRepository):
    def __init__(self, model_path: str = "ml_models/cardiovascular_model.pkl"):
        self.model = joblib.load(model_path)
        self.feature_names = [
            'age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo',
            'cholesterol', 'gluc', 'smoke', 'alco', 'active'
        ]
    
    async def predict_risk(self, patient_data: PatientData) -> RiskPrediction:
        features = self._patient_to_features(patient_data)
        features_df = pd.DataFrame([features], columns=self.feature_names)
        
        # Predição de probabilidade
        proba = self.model.predict_proba(features_df)[0]
        prediction = self.model.predict(features_df)[0]
        
        # Converter para RiskLevel
        risk_level = self._convert_to_risk_level(prediction, proba)
        
        # Calcular fatores de risco
        factors = self._calculate_risk_factors(patient_data, features)
        
        # Usar probabilidade da classe de risco (índice 1)
        risk_probability = proba[1] if len(proba) > 1 else max(proba)
        
        return RiskPrediction(
            risk_level=risk_level,
            probability=float(risk_probability),
            confidence=float(max(proba) - min(proba)),
            factors=factors
        )
    
    async def analyze_variable_impact(self, patient_data: PatientData, variable: str, new_value: float) -> dict:
        original_features = self._patient_to_features(patient_data)
        modified_features = original_features.copy()
        
        # Modificar a variável específica
        var_index = self.feature_names.index(variable)
        modified_features[var_index] = new_value
        
        # Predições
        original_df = pd.DataFrame([original_features], columns=self.feature_names)
        modified_df = pd.DataFrame([modified_features], columns=self.feature_names)
        
        original_proba = self.model.predict_proba(original_df)[0]
        modified_proba = self.model.predict_proba(modified_df)[0]
        
        # Calcular impacto
        impact = float(max(modified_proba) - max(original_proba))
        new_prediction = self.model.predict(modified_df)[0]
        new_risk = self._convert_to_risk_level(new_prediction, modified_proba)
        
        return {
            'impact': impact,
            'new_risk': new_risk,
            'explanation': self._generate_explanation(variable, impact, new_risk)
        }
    
    def _patient_to_features(self, patient_data: PatientData) -> list:
        return [
            patient_data.age,
            patient_data.gender,
            patient_data.height,
            patient_data.weight,
            patient_data.ap_hi,
            patient_data.ap_lo,
            patient_data.cholesterol,
            patient_data.gluc,
            patient_data.smoke,
            patient_data.alco,
            patient_data.active
        ]
    
    def _convert_to_risk_level(self, prediction: int, proba: np.ndarray) -> RiskLevel:
        # Usar a probabilidade da classe positiva (risco cardiovascular)
        risk_proba = proba[1] if len(proba) > 1 else max(proba)
        
        if risk_proba < 0.3:
            return RiskLevel.LOW
        elif risk_proba < 0.6:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH
    
    def _calculate_risk_factors(self, patient_data: PatientData, features: list) -> dict:
        factors = {}
        
        # Idade
        if patient_data.age > 60:
            factors['idade'] = 'Alto risco devido à idade avançada'
        
        # Colesterol
        if patient_data.cholesterol > 2:
            factors['colesterol'] = 'Colesterol acima do normal'
        
        # Pressão arterial sistólica
        if patient_data.ap_hi > 140:
            factors['pressao_sistolica'] = 'Pressão sistólica elevada'
            
        # Pressão arterial diastólica
        if patient_data.ap_lo > 90:
            factors['pressao_diastolica'] = 'Pressão diastólica elevada'
        
        # Glicose
        if patient_data.gluc > 1:
            factors['glicose'] = 'Glicose acima do normal'
            
        # Tabagismo
        if patient_data.smoke == 1:
            factors['tabagismo'] = 'Fumante - fator de risco cardiovascular'
            
        # IMC
        if patient_data.height > 0:
            bmi = patient_data.weight / ((patient_data.height / 100) ** 2)
            if bmi > 30:
                factors['obesidade'] = f'IMC elevado ({bmi:.1f}) - obesidade'
            elif bmi > 25:
                factors['sobrepeso'] = f'IMC elevado ({bmi:.1f}) - sobrepeso'
        
        return factors
    
    def _generate_explanation(self, variable: str, impact: float, new_risk: RiskLevel) -> str:
        explanations = {
            'age': f'Alteração na idade resultou em impacto de {impact:.2f} no risco',
            'gender': f'Mudança no gênero alterou o risco em {impact:.2f}',
            'height': f'Modificação na altura impactou em {impact:.2f}',
            'weight': f'Alteração no peso resultou em impacto de {impact:.2f}',
            'ap_hi': f'Mudança na pressão sistólica alterou o risco em {impact:.2f}',
            'ap_lo': f'Modificação na pressão diastólica impactou em {impact:.2f}',
            'cholesterol': f'Alteração no nível de colesterol resultou em impacto de {impact:.2f}',
            'gluc': f'Mudança na glicose alterou o risco em {impact:.2f}',
            'smoke': f'Alteração no status de fumante impactou em {impact:.2f}',
            'alco': f'Mudança no consumo de álcool alterou o risco em {impact:.2f}',
            'active': f'Modificação na atividade física impactou em {impact:.2f}'
        }
        
        return explanations.get(variable, f'Variável {variable} teve impacto de {impact:.2f}')