#!/bin/bash
# Script para iniciar os serviços

echo "=== Configurando Backend Service ==="
sudo cp /home/ubuntu/MLTCC/deploy/backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable backend
sudo systemctl start backend

echo "=== Configurando Nginx ==="
sudo cp /home/ubuntu/MLTCC/deploy/nginx.conf /etc/nginx/sites-available/cardiolearn
sudo ln -sf /etc/nginx/sites-available/cardiolearn /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "=== Status dos Serviços ==="
sudo systemctl status backend --no-pager
sudo systemctl status nginx --no-pager

echo "=== Serviços iniciados! ==="
echo "Acesse: http://SEU_IP_PUBLICO"
