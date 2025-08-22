#!/bin/bash

# Скрипт для настройки тестового приложения API Avito
# Выполните: chmod +x setup.sh && ./setup.sh

set -e

echo "🚀 Настройка тестового приложения API Avito"
echo "=========================================="

# Проверка на root права
if [[ $EUID -eq 0 ]]; then
   echo "❌ Не запускайте скрипт от имени root"
   exit 1
fi

# Обновление системы
echo "📦 Обновление системы..."
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
echo "📦 Установка зависимостей..."
sudo apt install -y python3 python3-pip python3-venv nginx curl git

# Установка Node.js
echo "📦 Установка Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Установка Certbot для SSL
echo "📦 Установка Certbot..."
sudo apt install -y certbot python3-certbot-nginx

# Создание директории для приложения
echo "📁 Создание директории приложения..."
sudo mkdir -p /var/www/avito-api-test
sudo chown $USER:$USER /var/www/avito-api-test

# Копирование файлов (если они находятся в текущей директории)
if [ -f "app.py" ]; then
    echo "📋 Копирование файлов приложения..."
    cp -r * /var/www/avito-api-test/
fi

# Переход в директорию приложения
cd /var/www/avito-api-test

# Создание виртуального окружения
echo "🐍 Создание виртуального окружения Python..."
python3 -m venv venv
source venv/bin/activate

# Установка Python зависимостей
echo "📦 Установка Python зависимостей..."
pip install -r requirements.txt

# Создание необходимых директорий
echo "📁 Создание директорий..."
mkdir -p logs uploads

# Создание файла .env если его нет
if [ ! -f ".env" ]; then
    echo "⚙️ Создание файла .env..."
    cp .env.example .env
    echo "⚠️  ВНИМАНИЕ: Отредактируйте файл .env и добавьте ваши API ключи Avito"
fi

# Настройка nginx
echo "🌐 Настройка nginx..."
sudo tee /etc/nginx/sites-available/ps-crm.ru > /dev/null <<EOF
server {
    listen 80;
    server_name ps-crm.ru www.ps-crm.ru;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ps-crm.ru www.ps-crm.ru;

    ssl_certificate /etc/letsencrypt/live/ps-crm.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ps-crm.ru/privkey.pem;

    root /var/www/avito-api-test/static;
    index index.html;

    location / {
        try_files \$uri \$uri/ @backend;
    }

    location @backend {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /webhook/avito {
        proxy_pass http://127.0.0.1:8000/webhook/avito;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Активация конфигурации nginx
sudo ln -sf /etc/nginx/sites-available/ps-crm.ru /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Создание systemd сервиса
echo "🔧 Создание systemd сервиса..."
sudo tee /etc/systemd/system/avito-api-test.service > /dev/null <<EOF
[Unit]
Description=Avito API Test Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/var/www/avito-api-test
Environment=PATH=/var/www/avito-api-test/venv/bin
ExecStart=/var/www/avito-api-test/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Перезагрузка systemd и активация сервиса
sudo systemctl daemon-reload
sudo systemctl enable avito-api-test

# Настройка прав доступа
echo "🔐 Настройка прав доступа..."
sudo chown -R $USER:$USER /var/www/avito-api-test
chmod +x /var/www/avito-api-test

echo ""
echo "✅ Настройка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте файл .env и добавьте ваши API ключи Avito"
echo "2. Получите SSL сертификат: sudo certbot --nginx -d ps-crm.ru -d www.ps-crm.ru"
echo "3. Запустите приложение: sudo systemctl start avito-api-test"
echo "4. Проверьте статус: sudo systemctl status avito-api-test"
echo "5. Откройте в браузере: https://ps-crm.ru"
echo ""
echo "📝 Полезные команды:"
echo "- Просмотр логов: sudo journalctl -u avito-api-test -f"
echo "- Перезапуск: sudo systemctl restart avito-api-test"
echo "- Остановка: sudo systemctl stop avito-api-test"
echo ""
echo "🔗 Webhook URL для настройки в Avito: https://ps-crm.ru/webhook/avito"