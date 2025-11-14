# Quick Start - Deploy AWS

## Passo a Passo Completo

### 1. Criar EC2 na AWS Console
- **AMI**: Ubuntu 22.04 LTS
- **Tipo**: t2.medium (mínimo)
- **Security Group**: Configurar regras de entrada:
  - SSH (22) - Seu IP
  - HTTP (80) - 0.0.0.0/0
  - HTTPS (443) - 0.0.0.0/0
  - Custom TCP (8000) - 0.0.0.0/0 (opcional, para testes)
- **Baixar arquivo .pem**

### 2. Conectar ao Servidor

**Opção A: AWS Console (Recomendado - Mais Fácil)**
```bash
# 1. AWS Console → EC2 → Instances
# 2. Selecione sua instância
# 3. Clique em "Connect"
# 4. Aba "EC2 Instance Connect"
# 5. Clique em "Connect"
# Abrirá um terminal no navegador
```

### 3. Pegar IP Público (se não souber)
```bash
curl -s http://checkip.amazonaws.com
```

### 4. Instalar Tecnologias no Servidor
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e ferramentas
sudo apt install -y python3 python3-venv python3-full python3-pip
python3 --version  # Verificar versão (deve ser 3.10+)

# Instalar Node.js e npm
sudo apt install -y nodejs npm
node --version     # Verificar versão (deve ser 18+)
npm --version

# Instalar Nginx (servidor web)
sudo apt install -y nginx
nginx -v          # Verificar versão

# Instalar Git
sudo apt install -y git
git --version

# Verificar se tudo foi instalado
echo "✅ Instalações concluídas!"
echo "Python: $(python3 --version)"
echo "Node: $(node --version)"
echo "NPM: $(npm --version)"
echo "Nginx: $(nginx -v 2>&1)"
echo "Git: $(git --version)"
```

### 5. Clonar e Configurar Projeto
```bash
# Clonar repositório
cd /home/ubuntu
git clone https://github.com/PauloDudu/MLTCC.git
cd MLTCC
git checkout dev_sqlite
```

### 6. Configurar Backend
```bash
cd /home/ubuntu/MLTCC/backend

# Criar virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
pip install --upgrade pip
pip install -r requirements.txt

# Treinar modelo ML
cd ml_models
python train_model.py
cd ..

# Executar migrations
python -m alembic upgrade head

# Configurar variáveis de ambiente
cp .env.example .env
nano .env
# Adicione: GROQ_API_KEY="sua_chave_aqui"
# Salve: Ctrl+O, Enter, Ctrl+X
```

### 7. Configurar Frontend
```bash
cd /home/ubuntu/MLTCC/frontend

# Configurar URL da API
cp .env.local.example .env.local 2>/dev/null || touch .env.local
nano .env.local
# Adicione: VUE_APP_API_URL=http://SEU_IP_PUBLICO/api/v1
# Substitua SEU_IP_PUBLICO pelo IP da EC2
# Salve: Ctrl+O, Enter, Ctrl+X

# Instalar dependências e buildar
npm install
npm run build

# Verificar se build foi criado
ls -la dist/
```

### 8. Configurar Permissões
```bash
# Dar permissão ao nginx para acessar os arquivos
sudo chmod 755 /home/ubuntu
sudo chmod 755 /home/ubuntu/MLTCC
sudo chmod 755 /home/ubuntu/MLTCC/frontend
sudo chmod -R 755 /home/ubuntu/MLTCC/frontend/dist
```

### 9. Configurar Serviço Backend (Systemd)
```bash
cd /home/ubuntu/MLTCC/deploy

# Copiar arquivo de serviço
sudo cp backend.service /etc/systemd/system/

# Recarregar systemd e iniciar serviço
sudo systemctl daemon-reload
sudo systemctl enable backend
sudo systemctl start backend

# Verificar status
sudo systemctl status backend

# Se houver erro, ver logs:
# sudo journalctl -u backend -n 50 --no-pager
```

### 10. Configurar Nginx
```bash
cd /home/ubuntu/MLTCC/deploy

# Criar diretórios se não existirem
sudo mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled

# Copiar configuração
sudo cp nginx.conf /etc/nginx/sites-available/cardiolearn

# Criar link simbólico
sudo ln -sf /etc/nginx/sites-available/cardiolearn /etc/nginx/sites-enabled/

# Remover configuração padrão
sudo rm -f /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Reiniciar nginx
sudo systemctl restart nginx

# Verificar status
sudo systemctl status nginx
```

### 11. Verificar Funcionamento
```bash
# Testar backend
curl http://localhost:8000/health
# Deve retornar: {"status":"healthy"}

# Testar frontend via nginx
curl -I http://localhost
# Deve retornar: HTTP/1.1 200 OK

# Ver logs em tempo real (se necessário)
sudo journalctl -u backend -f
sudo tail -f /var/log/nginx/error.log
```

### 12. Acessar Aplicação
```
http://SEU_IP_PUBLICO
```

## 🔧 Comandos Úteis

### Reiniciar Serviços
```bash
sudo systemctl restart backend
sudo systemctl restart nginx
```

### Ver Logs
```bash
# Backend
sudo journalctl -u backend -n 100 --no-pager
sudo journalctl -u backend -f  # Tempo real

# Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Atualizar Aplicação
```bash
cd /home/ubuntu/MLTCC
git pull

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart backend

# Frontend
cd ../frontend
npm install
npm run build
sudo systemctl restart nginx
```

### Parar Serviços
```bash
sudo systemctl stop backend
sudo systemctl stop nginx
```

## ⚠️ Troubleshooting

### Backend não inicia
```bash
# Verificar logs
sudo journalctl -u backend -n 50 --no-pager

# Testar manualmente
cd /home/ubuntu/MLTCC/backend
source venv/bin/activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Nginx erro 500
```bash
# Verificar permissões
ls -la /home/ubuntu/MLTCC/frontend/dist/
sudo chmod -R 755 /home/ubuntu/MLTCC/frontend/dist

# Ver logs de erro
sudo tail -20 /var/log/nginx/error.log
```

### Porta 80 não acessível
```bash
# Verificar Security Group na AWS Console
# Deve ter regra HTTP (80) com source 0.0.0.0/0

# Verificar se nginx está rodando
sudo systemctl status nginx
sudo netstat -tlnp | grep :80
```


