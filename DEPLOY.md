# 🚀 Deploy no Railway

## 📋 Deploy via GitHub (Recomendado)

1. **Conectar repositório:**
   - Acesse railway.app
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha este repositório

2. **Criar 2 serviços:**
   - **Backend**: Root Directory = `backend`
   - **Frontend**: Root Directory = `frontend`

3. **Variáveis de ambiente:**
   - **Backend**: `GROQ_API_KEY`
   - **Frontend**: `VUE_APP_API_URL` (URL do backend)

## 🔗 URLs Finais
- **Backend**: https://seu-backend.railway.app
- **Frontend**: https://seu-frontend.railway.app

## ⚙️ Configuração Automática
Os arquivos `railway.toml` detectam automaticamente as pastas corretas.