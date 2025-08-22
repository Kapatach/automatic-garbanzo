# Тестовое приложение для API Avito

Это веб-приложение для тестирования интеграции с API Avito. Позволяет получать и отправлять сообщения через API Avito.

## 📋 Содержание

1. [Предварительные требования](#предварительные-требования)
2. [Настройка проекта](#настройка-проекта)
3. [Получение API ключей Avito](#получение-api-ключей-avito)
4. [Настройка сервера](#настройка-сервера)
5. [Запуск приложения](#запуск-приложения)
6. [Использование приложения](#использование-приложения)
7. [Устранение неполадок](#устранение-неполадок)

## 🔧 Предварительные требования

- Ubuntu 22.04
- Python 3.8+
- Node.js 16+ (для сборки фронтенда)
- Домен ps-crm.ru
- SSL сертификат (для HTTPS)

## 🚀 Настройка проекта

### 1. Установка зависимостей

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Установка Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Установка nginx
sudo apt install nginx -y
```

### 2. Клонирование проекта

```bash
cd /var/www/
sudo git clone <your-repo-url> avito-api-test
sudo chown -R $USER:$USER avito-api-test
cd avito-api-test
```

### 3. Настройка Python окружения

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔑 Получение API ключей Avito

### 1. Регистрация в Avito API

1. Перейдите на [Avito API Developer Portal](https://developers.avito.ru/)
2. Зарегистрируйтесь как разработчик
3. Создайте новое приложение
4. Получите следующие ключи:
   - `CLIENT_ID` - ID вашего приложения
   - `CLIENT_SECRET` - секретный ключ
   - `ACCESS_TOKEN` - токен доступа

### 2. Настройка webhook URL

В настройках приложения Avito укажите webhook URL:
```
https://ps-crm.ru/webhook/avito
```

## ⚙️ Настройка сервера

### 1. Настройка nginx

Создайте конфигурацию nginx:

```bash
sudo nano /etc/nginx/sites-available/ps-crm.ru
```

Содержимое файла:

```nginx
server {
    listen 80;
    server_name ps-crm.ru www.ps-crm.ru;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ps-crm.ru www.ps-crm.ru;

    ssl_certificate /etc/letsencrypt/live/ps-crm.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ps-crm.ru/privkey.pem;

    root /var/www/avito-api-test/static;
    index index.html;

    location / {
        try_files $uri $uri/ @backend;
    }

    location @backend {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /webhook/avito {
        proxy_pass http://127.0.0.1:8000/webhook/avito;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Получение SSL сертификата

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d ps-crm.ru -d www.ps-crm.ru
```

### 3. Активация конфигурации

```bash
sudo ln -s /etc/nginx/sites-available/ps-crm.ru /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🏃‍♂️ Запуск приложения

### 1. Настройка переменных окружения

Создайте файл `.env`:

```bash
cp .env.example .env
nano .env
```

Заполните переменные:

```env
AVITO_CLIENT_ID=your_client_id
AVITO_CLIENT_SECRET=your_client_secret
AVITO_ACCESS_TOKEN=your_access_token
AVITO_WEBHOOK_SECRET=your_webhook_secret
FLASK_SECRET_KEY=your_flask_secret_key
```

### 2. Запуск приложения

```bash
# Активация виртуального окружения
source venv/bin/activate

# Запуск в режиме разработки
python app.py

# Или запуск через gunicorn для продакшена
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

### 3. Настройка systemd сервиса

Создайте файл сервиса:

```bash
sudo nano /etc/systemd/system/avito-api-test.service
```

Содержимое:

```ini
[Unit]
Description=Avito API Test Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/avito-api-test
Environment=PATH=/var/www/avito-api-test/venv/bin
ExecStart=/var/www/avito-api-test/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Активируйте сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable avito-api-test
sudo systemctl start avito-api-test
```

## 📱 Использование приложения

### 1. Открытие приложения

Перейдите в браузере по адресу: `https://ps-crm.ru`

### 2. Основные функции

- **Получение сообщений**: Просмотр входящих сообщений из Avito
- **Отправка сообщений**: Отправка сообщений через API Avito
- **Логи**: Просмотр логов взаимодействия с API
- **Статус**: Проверка статуса подключения к API

### 3. Тестирование webhook

1. Отправьте тестовое сообщение через Avito
2. Проверьте получение webhook в разделе "Логи"
3. Убедитесь, что сообщение отображается в списке

## 🔧 Устранение неполадок

### Проблемы с подключением к API

1. Проверьте правильность API ключей в `.env`
2. Убедитесь, что токен не истек
3. Проверьте права доступа приложения в Avito

### Проблемы с webhook

1. Проверьте доступность URL `https://ps-crm.ru/webhook/avito`
2. Убедитесь, что nginx правильно проксирует запросы
3. Проверьте логи приложения: `sudo journalctl -u avito-api-test`

### Проблемы с SSL

1. Проверьте срок действия сертификата: `sudo certbot certificates`
2. Обновите сертификат: `sudo certbot renew`

## 📁 Структура проекта

```
avito-api-test/
├── app.py                 # Основное Flask приложение
├── avito_api.py          # Модуль для работы с API Avito
├── requirements.txt      # Python зависимости
├── static/              # Статические файлы
│   ├── index.html       # Главная страница
│   ├── style.css        # Стили
│   └── script.js        # JavaScript
├── templates/           # HTML шаблоны
├── logs/               # Логи приложения
├── .env                # Переменные окружения
└── README.md           # Документация
```

## 🔒 Безопасность

- Все API ключи хранятся в переменных окружения
- Используется HTTPS для всех соединений
- Webhook проверяется на подлинность
- Логи не содержат чувствительной информации

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Убедитесь в правильности настройки
3. Обратитесь к документации Avito API