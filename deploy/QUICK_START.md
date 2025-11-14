# Quick Start - Deploy AWS

## Passo a Passo Rápido

### 1. Criar EC2 na AWS Console
- Ubuntu 22.04 LTS
- t2.medium
- Security Group: portas 22, 80, 443 abertas
- Baixar arquivo .pem

### 2. Conectar via SSH
```bash
chmod 400 sua-chave.pem
ssh -i sua-chave.pem ubuntu@SEU_IP_PUBLICO
```

### 3. Executar comandos na EC2
```bash
# Instalar dependências
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3-pip nodejs npm nginx git

# Clonar projeto
cd /home/ubuntu
git clone https://github.com/PauloDudu/MLTCC.git
cd MLTCC
git checkout dev_sqlite

# Backend
cd backend
pip3 install -r requirements.txt
cd ml_models && python3 train_model.py && cd ..
python3 -m alembic upgrade head

# Configurar .env
nano .env
# Adicione: GROQ_API_KEY="sua_chave"

# Frontend
cd ../frontend
nano .env.local
# Altere para: VUE_APP_API_URL=http://SEU_IP_PUBLICO/api/v1
npm install
npm run build

# Configurar serviços
cd ../deploy
sudo cp backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable backend
sudo systemctl start backend

# Configurar Nginx
sudo cp nginx.conf /etc/nginx/sites-available/cardiolearn
sudo ln -sf /etc/nginx/sites-available/cardiolearn /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

### 4. Acessar
```
http://SEU_IP_PUBLICO
```

## Verificar Status
```bash
sudo systemctl status backend
sudo systemctl status nginx
curl http://localhost:8000/health
```
