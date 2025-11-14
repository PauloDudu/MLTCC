#!/bin/bash
# Script de setup para AWS EC2 Ubuntu

echo "=== Atualizando sistema ==="
sudo apt update && sudo apt upgrade -y

echo "=== Instalando Python 3.11 ==="
sudo apt install -y python3.11 python3.11-venv python3-pip

echo "=== Instalando Node.js 18 ==="
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

echo "=== Instalando Nginx ==="
sudo apt install -y nginx

echo "=== Clonando repositório ==="
cd /home/ubuntu
git clone https://github.com/PauloDudu/MLTCC.git
cd MLTCC
git checkout dev_sqlite

echo "=== Configurando Backend ==="
cd backend
python3 -m pip install -r requirements.txt
cd ml_models && python3 train_model.py && cd ..
python3 -m alembic upgrade head

echo "=== Configurando Frontend ==="
cd ../frontend
npm install
npm run build

echo "=== Setup concluído! ==="
