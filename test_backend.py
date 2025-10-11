#!/usr/bin/env python3
"""Script para testar o backend localmente"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from backend.src.main import app
    print("✅ Backend importado com sucesso!")
    
    # Testar se as rotas estão configuradas
    routes = [route.path for route in app.routes]
    print(f"✅ Rotas encontradas: {routes}")
    
    # Testar dependências
    from backend.src.infrastructure.ml_model import ScikitLearnMLRepository
    ml_repo = ScikitLearnMLRepository()
    print("✅ ML Repository inicializado com sucesso!")
    
    print("\n🎉 Backend está funcionando! Para executar:")
    print("cd backend && python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
    
except Exception as e:
    print(f"❌ Erro no backend: {e}")
    import traceback
    traceback.print_exc()