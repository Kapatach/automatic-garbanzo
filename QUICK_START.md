# 🚀 Быстрый старт - Тестирование API Avito

## ⚡ Быстрая настройка (5 минут)

### 1. Клонирование и настройка
```bash
# Клонируйте проект на сервер
git clone <your-repo-url> /var/www/avito-api-test
cd /var/www/avito-api-test

# Запустите автоматическую настройку
chmod +x setup.sh
./setup.sh
```

### 2. Настройка API ключей
```bash
# Отредактируйте файл с переменными окружения
nano .env
```

Добавьте ваши ключи Avito:
```env
AVITO_CLIENT_ID=your_client_id_here
AVITO_CLIENT_SECRET=your_client_secret_here
AVITO_ACCESS_TOKEN=your_access_token_here
AVITO_WEBHOOK_SECRET=your_webhook_secret_here
FLASK_SECRET_KEY=your_secret_key_here
```

### 3. Получение SSL сертификата
```bash
sudo certbot --nginx -d ps-crm.ru -d www.ps-crm.ru
```

### 4. Запуск приложения
```bash
sudo systemctl start avito-api-test
sudo systemctl status avito-api-test
```

### 5. Открытие в браузере
Перейдите по адресу: **https://ps-crm.ru**

## 📋 Что умеет приложение

✅ **Получение сообщений** - просмотр входящих сообщений из Avito  
✅ **Отправка сообщений** - отправка сообщений через API Avito  
✅ **Управление чатами** - просмотр и управление чатами  
✅ **Webhook обработка** - автоматическое получение уведомлений  
✅ **Загрузка файлов** - отправка вложений  
✅ **Логирование** - подробные логи всех операций  
✅ **Современный UI** - красивый и удобный интерфейс  

## 🔧 Основные команды

```bash
# Статус приложения
sudo systemctl status avito-api-test

# Запуск/остановка
sudo systemctl start avito-api-test
sudo systemctl stop avito-api-test
sudo systemctl restart avito-api-test

# Просмотр логов
sudo journalctl -u avito-api-test -f

# Обновление приложения
cd /var/www/avito-api-test
git pull
sudo systemctl restart avito-api-test
```

## 🌐 Webhook URL для Avito

```
https://ps-crm.ru/webhook/avito
```

## 📞 Поддержка

- 📖 **Подробная документация**: [README.md](README.md)
- 🔑 **Настройка API ключей**: [AVITO_API_SETUP.md](AVITO_API_SETUP.md)
- 🐛 **Логи приложения**: Вкладка "Логи" в веб-интерфейсе
- 🔧 **Системные логи**: `sudo journalctl -u avito-api-test -f`

## ⚠️ Важные замечания

1. **Безопасность**: Никогда не коммитьте файл `.env` в git
2. **SSL**: Обязательно настройте SSL сертификат для webhook
3. **Мониторинг**: Регулярно проверяйте логи приложения
4. **Обновления**: Поддерживайте систему в актуальном состоянии

## 🎯 Следующие шаги

1. Получите API ключи Avito (см. [AVITO_API_SETUP.md](AVITO_API_SETUP.md))
2. Настройте webhook в личном кабинете Avito
3. Протестируйте отправку и получение сообщений
4. Настройте мониторинг и алерты
5. Интегрируйте в вашу CRM систему