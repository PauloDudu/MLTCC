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
        
        context = f"""Você é um assistente médico educacional especializado em cardiologia. Seja direto, use emojis e markdown para destacar informações importantes.

CASO ATUAL:
🧑 Idade: {patient_data['age']} anos | 🩺 Pressão: {patient_data['ap_hi']}/{patient_data['ap_lo']} mmHg
💊 Colesterol: {patient_data['cholesterol']} | 🏃 Ativo: {'Sim' if patient_data['active'] == 1 else 'Não'} | 🚬 Fumante: {'Sim' if patient_data['smoke'] == 1 else 'Não'}

📊 DIAGNÓSTICO: Risco {prediction['risk_level'].upper()} ({prediction['probability']*100:.1f}%)

REGRAS:
- Seja BREVE (máximo 3-4 linhas)
- Use emojis relevantes (❤️ 🩺 ⚠️ ✅ ❌)
- Use **negrito** para destacar pontos importantes
- Foque no que o estudante perguntou
- Seja conversacional e natural"""

        messages = [{"role": "system", "content": context}]
        
        for msg in chat_history[-4:]:
            messages.append({"role": msg['role'], "content": msg['content']})
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant",
                temperature=0.8,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except:
            return "Desculpe, não consegui processar sua pergunta. Tente reformular."
