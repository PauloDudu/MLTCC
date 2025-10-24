import os
from groq import Groq
from pathlib import Path

class AIChat:
    def __init__(self):
        env_path = Path(__file__).parent.parent.parent / '.env'
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if line.startswith('GROQ_API_KEY'):
                        key = line.split('=')[1].strip().strip('"')
                        os.environ['GROQ_API_KEY'] = key
        
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    def chat(self, message: str, patient_data: dict, prediction: dict, chat_history: list) -> str:
        """Chat contextualizado com dados do paciente"""
        
        # Mapear valores de colesterol e glicose
        cholesterol_map = {1: "Normal", 2: "Acima do normal", 3: "Muito acima"}
        glucose_map = {1: "Normal", 2: "Acima do normal", 3: "Muito acima"}
        
        # Calcular IMC
        height_m = patient_data['height'] / 100
        bmi = patient_data['weight'] / (height_m ** 2)
        
        context = f"""Você é um assistente médico educacional especializado em cardiologia. Seja direto, use emojis e markdown para destacar informações importantes.

CASO ATUAL - DADOS COMPLETOS:
🧑 **Paciente:** {patient_data['age']} anos, {'Feminino' if patient_data['gender'] == 1 else 'Masculino'}
📏 **Físico:** {patient_data['height']}cm, {patient_data['weight']}kg (IMC: {bmi:.1f})
🩺 **Pressão:** {patient_data['ap_hi']}/{patient_data['ap_lo']} mmHg
💊 **Colesterol:** {cholesterol_map.get(patient_data['cholesterol'], 'N/A')} (nível {patient_data['cholesterol']})
🍯 **Glicose:** {glucose_map.get(patient_data['gluc'], 'N/A')} (nível {patient_data['gluc']})
🏃 **Ativo:** {'Sim' if patient_data['active'] == 1 else 'Não'} | 🚬 **Fumante:** {'Sim' if patient_data['smoke'] == 1 else 'Não'} | 🍺 **Álcool:** {'Sim' if patient_data['alco'] == 1 else 'Não'}

📊 **DIAGNÓSTICO:** Risco {prediction['risk_level'].upper()} ({prediction['probability']*100:.1f}%)

REGRAS:
- Seja BREVE mas COMPLETE sempre seu raciocínio
- Use emojis relevantes (❤️ 🩺 ⚠️ ✅ ❌)
- Use **negrito** para destacar pontos importantes
- Foque no que o estudante perguntou
- SEMPRE termine com uma conclusão clara e completa"""

        messages = [{"role": "system", "content": context}]
        
        for msg in chat_history[-4:]:
            messages.append({"role": msg['role'], "content": msg['content']})
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant",
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except:
            return "Desculpe, não consegui processar sua pergunta. Tente reformular."
