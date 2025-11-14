#!/bin/bash
# Script para atualizar a aplicação

echo "=== Atualizando código ==="
cd /home/ubuntu/MLTCC
git pull origin dev_sqlite

echo "=== Atualizando Backend ==="
cd backend
python3 -m pip install -r requirements.txt
python3 -m alembic upgrade head
sudo systemctl restart backend

echo "=== Atualizando Frontend ==="
cd ../frontend
npm install
npm run build

echo "=== Reiniciando Nginx ==="
sudo systemctl restart nginx

echo "=== Aplicação atualizada! ==="
