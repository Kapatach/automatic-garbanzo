# 🚀 Пошаговая инструкция по запуску приложения API Avito

## 📋 Предварительные требования

- Ubuntu 22.04 сервер
- Домен ps-crm.ru (указан в A-записи на ваш сервер)
- SSH доступ к серверу
- Права sudo

## 🔧 Шаг 1: Подготовка сервера

### 1.1 Подключение к серверу
```bash
ssh username@your-server-ip
```

### 1.2 Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.3 Установка базовых пакетов
```bash
sudo apt install -y git curl wget nano
```

## 📥 Шаг 2: Клонирование проекта

### 2.1 Создание директории
```bash
sudo mkdir -p /var/www/avito-api-test
sudo chown $USER:$USER /var/www/avito-api-test
cd /var/www/avito-api-test
```

### 2.2 Клонирование (если проект в git)
```bash
git clone <your-repo-url> .
```

### 2.3 Или копирование файлов
Если файлы уже на сервере:
```bash
# Скопируйте все файлы проекта в /var/www/avito-api-test/
```

## ⚙️ Шаг 3: Автоматическая настройка

### 3.1 Запуск скрипта настройки
```bash
chmod +x setup.sh
./setup.sh
```

Скрипт автоматически:
- Установит все зависимости
- Настроит nginx
- Создаст systemd сервис
- Настроит права доступа

## 🔑 Шаг 4: Получение API ключей Avito

### 4.1 Регистрация в Avito API
1. Перейдите на [https://developers.avito.ru/](https://developers.avito.ru/)
2. Зарегистрируйтесь как разработчик
3. Создайте новое приложение

### 4.2 Получение ключей
В настройках приложения получите:
- Client ID
- Client Secret
- Access Token
- Webhook Secret

### 4.3 Настройка переменных окружения
```bash
nano .env
```

Заполните файл:
```env
AVITO_CLIENT_ID=your_client_id_here
AVITO_CLIENT_SECRET=your_client_secret_here
AVITO_ACCESS_TOKEN=your_access_token_here
AVITO_WEBHOOK_SECRET=your_webhook_secret_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=production
HOST=127.0.0.1
PORT=8000
```

## 🔒 Шаг 5: Настройка SSL сертификата

### 5.1 Получение сертификата
```bash
sudo certbot --nginx -d ps-crm.ru -d www.ps-crm.ru
```

### 5.2 Проверка SSL
```bash
sudo certbot certificates
```

## 🚀 Шаг 6: Запуск приложения

### 6.1 Запуск сервиса
```bash
sudo systemctl start avito-api-test
```

### 6.2 Проверка статуса
```bash
sudo systemctl status avito-api-test
```

### 6.3 Включение автозапуска
```bash
sudo systemctl enable avito-api-test
```

## 🌐 Шаг 7: Настройка webhook в Avito

### 7.1 В личном кабинете Avito API
1. Перейдите в настройки приложения
2. Найдите раздел "Webhook"
3. Добавьте URL: `https://ps-crm.ru/webhook/avito`
4. Выберите события для уведомлений
5. Сохраните настройки

### 7.2 Тестирование webhook
1. Нажмите "Тест webhook" в настройках
2. Проверьте логи приложения

## 🧪 Шаг 8: Тестирование приложения

### 8.1 Открытие в браузере
Перейдите по адресу: **https://ps-crm.ru**

### 8.2 Проверка функций
1. **Статус API** - должен быть зеленый индикатор
2. **Сообщения** - загрузите список сообщений
3. **Чаты** - просмотрите доступные чаты
4. **Отправка** - отправьте тестовое сообщение
5. **Логи** - проверьте работу логирования

### 8.3 Тестирование webhook
1. Отправьте сообщение через Avito
2. Проверьте получение в логах
3. Убедитесь, что сообщение появилось в списке

## 🔧 Шаг 9: Настройка мониторинга

### 9.1 Просмотр логов
```bash
# Логи приложения
sudo journalctl -u avito-api-test -f

# Логи nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 9.2 Настройка firewall
```bash
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 9.3 Автообновление SSL
```bash
sudo crontab -e
# Добавьте строку:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Шаг 10: Проверка работоспособности

### 10.1 Основные проверки
```bash
# Статус сервиса
sudo systemctl status avito-api-test

# Проверка портов
sudo netstat -tulpn | grep :8000

# Проверка nginx
sudo nginx -t
sudo systemctl status nginx

# Проверка SSL
curl -I https://ps-crm.ru
```

### 10.2 Тестирование API
```bash
# Проверка статуса API
curl https://ps-crm.ru/api/status

# Проверка webhook
curl https://ps-crm.ru/webhook/avito
```

## 🚨 Устранение неполадок

### Проблема: Приложение не запускается
```bash
# Проверка логов
sudo journalctl -u avito-api-test -n 50

# Проверка прав доступа
ls -la /var/www/avito-api-test/

# Проверка переменных окружения
cat .env
```

### Проблема: nginx не работает
```bash
# Проверка конфигурации
sudo nginx -t

# Перезапуск nginx
sudo systemctl restart nginx

# Проверка статуса
sudo systemctl status nginx
```

### Проблема: SSL сертификат не работает
```bash
# Проверка сертификата
sudo certbot certificates

# Обновление сертификата
sudo certbot renew

# Проверка nginx конфигурации
sudo nginx -t
```

### Проблема: API не отвечает
```bash
# Проверка переменных окружения
cat .env

# Проверка подключения к API
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.avito.ru/v1/chats
```

## 📞 Поддержка

### Полезные команды
```bash
# Перезапуск приложения
sudo systemctl restart avito-api-test

# Просмотр логов в реальном времени
sudo journalctl -u avito-api-test -f

# Проверка использования ресурсов
htop

# Проверка дискового пространства
df -h
```

### Документация
- [README.md](README.md) - Подробная документация
- [AVITO_API_SETUP.md](AVITO_API_SETUP.md) - Настройка API ключей
- [QUICK_START.md](QUICK_START.md) - Быстрый старт

## ✅ Проверочный список

- [ ] Сервер обновлен
- [ ] Проект склонирован
- [ ] Скрипт настройки выполнен
- [ ] API ключи получены и настроены
- [ ] SSL сертификат установлен
- [ ] Приложение запущено
- [ ] Webhook настроен в Avito
- [ ] Все функции протестированы
- [ ] Мониторинг настроен
- [ ] Firewall настроен

## 🎯 Результат

После выполнения всех шагов у вас будет:

✅ **Работающее приложение** на https://ps-crm.ru  
✅ **Полная интеграция** с API Avito  
✅ **Автоматические уведомления** через webhook  
✅ **Безопасное соединение** с SSL  
✅ **Мониторинг и логирование** всех операций  
✅ **Готовность к продакшену**  

Приложение готово к использованию и интеграции с вашей CRM системой!