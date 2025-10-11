# 🏥 Sistema de Ensino de Doenças Cardiovasculares

Sistema educacional baseado em Clean Architecture para auxiliar no ensino de medicina sobre doenças cardiovasculares, utilizando machine learning para predição de riscos.

## 🚀 Tecnologias

- **Backend**: Python + FastAPI
- **Frontend**: Vue.js 3 + Vuetify (Material Design)
- **ML**: scikit-learn
- **Database**: PostgreSQL
- **Containerização**: Docker + Docker Compose

## 📁 Estrutura do Projeto

```
MLTCC/
├── backend/                 # API FastAPI
│   ├── src/
│   │   ├── domain/         # Entidades e regras de negócio
│   │   ├── application/    # Casos de uso
│   │   ├── infrastructure/ # Implementações externas
│   │   └── interfaces/     # Contratos/Interfaces
│   ├── ml_models/          # Modelos treinados
│   └── requirements.txt
├── frontend/               # Vue.js App
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── services/
│   │   └── router/
│   └── package.json
├── docker-compose.yml
└── .github/workflows/      # CI/CD
```

## 🏃♂️ Como Executar

### Opção 1: VS Code (Recomendado)
1. Abra o projeto no VS Code
2. Pressione `F5` ou `Ctrl+Shift+P` → `Tasks: Run Task` → `Start Full Application`

### Opção 2: Manual
```bash
# Backend
cd backend
py -m pip install -r requirements.txt
cd ml_models && py train_model.py && cd ..
py -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (novo terminal)
cd frontend
npm install
npm run serve
```

### Opção 3: Docker
```bash
docker-compose up --build
```

## 🌐 Acessos
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

## 🎯 Funcionalidades

1. **Predição de Risco**: Inserir dados clínicos e obter predição de risco cardiovascular
2. **Casos Clínicos**: Casos fictícios para prática e comparação com IA
3. **Estudo Interativo**: Análise em tempo real do impacto de variáveis no risco

## 📋 Pré-requisitos

- **Python 3.11+**: https://python.org/downloads/
- **Node.js 18+**: https://nodejs.org/
- **Docker** (opcional): https://docker.com/

## 🏗️ Arquitetura

O projeto segue os princípios da **Clean Architecture**:

- **Domain**: Entidades e regras de negócio
- **Application**: Casos de uso e orquestração
- **Infrastructure**: Implementações de ML e dados
- **Interfaces**: Controllers e DTOs da API