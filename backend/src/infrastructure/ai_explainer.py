import os
from groq import Groq
from pathlib import Path

class AIExplainer:
    def __init__(self):
        env_path = Path(__file__).parent.parent.parent / '.env'
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if line.startswith('GROQ_API_KEY'):
                        key = line.split('=')[1].strip().strip('"')
                        os.environ['GROQ_API_KEY'] = key
        
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )
    
    def generate_explanation(self, patient_data: dict, risk_level: str, probability: float, factors: dict) -> str:
        """Gera explicação personalizada usando IA"""
        
        # Sempre retornar explicação padrão por enquanto (mais rápido e confiável)
        return self._get_default_explanation(risk_level, patient_data)
    
    def _get_default_explanation(self, risk_level: str, patient_data: dict) -> str:
        """Explicação padrão caso a API falhe"""
        if risk_level == 'baixo':
            return f"O paciente apresenta fatores favoráveis como idade de {patient_data['age']} anos e pressão arterial controlada, resultando em baixo risco cardiovascular."
        elif risk_level == 'medio':
            return f"Alguns fatores como pressão arterial de {patient_data['ap_hi']}/{patient_data['ap_lo']} mmHg indicam necessidade de acompanhamento médico regular."
        else:
            return f"Múltiplos fatores de risco foram identificados, incluindo idade de {patient_data['age']} anos e pressão arterial elevada, indicando alto risco cardiovascular."
