# 🛠️ Guia de Instalação

## 📋 Pré-requisitos

### **Python 3.11+**
- **Download**: https://www.python.org/downloads/
- ⚠️ **IMPORTANTE**: Marcar "Add Python to PATH" durante instalação

### **Node.js 18+**
- **Download**: https://nodejs.org/
- Recomendado: versão LTS (Long Term Support)

## ✅ Verificar Instalação

```bash
# Verificar Python
py --version

# Verificar Node.js
node --version

# Verificar npm
npm --version
```

## 🚀 Instalação e Execução

### **Método 1: VS Code (Recomendado)**

1. **Abrir projeto no VS Code**
2. **Pressionar F5** ou usar menu de tarefas
3. **Selecionar**: `Start Full Application`

### **Método 2: Manual**

```bash
# 1. Backend
cd backend
py -m pip install -r requirements.txt
cd ml_models
py train_model.py
cd ..
py -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 2. Frontend (novo terminal)
cd frontend
npm install
npm run serve
```

### **Método 3: Docker**

```bash
# Instalar Docker Desktop primeiro
docker-compose up --build
```

## 🌐 Acessos

- **Frontend**: http://localhost:8080
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Solução de Problemas

### **Python não encontrado**
- Reinstalar Python marcando "Add to PATH"
- Usar `py` em vez de `python`

### **Erro de CORS**
- Verificar se backend está na porta 8000
- Frontend deve estar na porta 8080

### **Dependências não instaladas**
```bash
# Backend
cd backend && py -m pip install -r requirements.txt

# Frontend  
cd frontend && npm install
```