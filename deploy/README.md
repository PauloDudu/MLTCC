# Deploy AWS EC2 - CardioLearn AI

## 1. Criar EC2 na AWS

### Configurações da Instância:
- **AMI**: Ubuntu Server 22.04 LTS
- **Tipo**: t2.medium (mínimo t2.small)
- **Storage**: 20 GB
- **Security Group**: Abrir portas 22 (SSH), 80 (HTTP), 443 (HTTPS)

### Regras do Security Group:
```
Type        Protocol    Port    Source
SSH         TCP         22      Seu IP
HTTP        TCP         80      0.0.0.0/0
HTTPS       TCP         443     0.0.0.0/0
```

## 2. Conectar na EC2

```bash
# Baixe o arquivo .pem da AWS
chmod 400 sua-chave.pem
ssh -i sua-chave.pem ubuntu@SEU_IP_PUBLICO
```

## 3. Executar Setup Inicial

```bash
# Baixar script de setup
wget https://raw.githubusercontent.com/PauloDudu/MLTCC/dev_sqlite/deploy/setup_aws.sh
chmod +x setup_aws.sh
./setup_aws.sh
```

## 4. Configurar Variáveis de Ambiente

```bash
cd /home/ubuntu/MLTCC/backend
nano .env
```

Adicione:
```
GROQ_API_KEY="sua_chave_groq_aqui"
DATABASE_URL="sqlite:///./cardio_ml.db"
```

## 5. Atualizar Frontend para usar IP da AWS

```bash
cd /home/ubuntu/MLTCC/frontend
nano .env.local
```

Altere para:
```
VUE_APP_API_URL=http://SEU_IP_PUBLICO/api/v1
```

Rebuild:
```bash
npm run build
```

## 6. Iniciar Serviços

```bash
cd /home/ubuntu/MLTCC/deploy
chmod +x start_services.sh
./start_services.sh
```

## 7. Acessar Aplicação

Abra no navegador:
```
http://SEU_IP_PUBLICO
```

## Comandos Úteis

### Ver logs do backend:
```bash
sudo journalctl -u backend -f
```

### Ver logs do nginx:
```bash
sudo tail -f /var/log/nginx/error.log
```

### Reiniciar serviços:
```bash
sudo systemctl restart backend
sudo systemctl restart nginx
```

### Atualizar aplicação:
```bash
cd /home/ubuntu/MLTCC/deploy
./update_app.sh
```

### Verificar status:
```bash
sudo systemctl status backend
sudo systemctl status nginx
```

## Troubleshooting

### Backend não inicia:
```bash
cd /home/ubuntu/MLTCC/backend
python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Verificar portas:
```bash
sudo netstat -tulpn | grep -E ':(80|8000)'
```

### Testar API:
```bash
curl http://localhost:8000/health
```

## Opcional: Configurar HTTPS com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seu-dominio.com
```
