"""
Основное Flask приложение для тестирования API Avito
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import logging
from datetime import datetime
import os
from dotenv import load_dotenv
from avito_api import avito_api

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Создаем папку для логов если её нет
os.makedirs('logs', exist_ok=True)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
CORS(app)

# Глобальная переменная для хранения логов
app_logs = []

def add_log(level: str, message: str, data: dict = None):
    """Добавление записи в лог"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'level': level,
        'message': message,
        'data': data
    }
    app_logs.append(log_entry)
    
    # Ограничиваем количество логов
    if len(app_logs) > 1000:
        app_logs.pop(0)
    
    logger.info(f"{level.upper()}: {message}")

@app.route('/')
def index():
    """Главная страница"""
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Статические файлы"""
    return send_from_directory('static', filename)

@app.route('/api/status')
def api_status():
    """Проверка статуса подключения к API Avito"""
    try:
        status = avito_api.get_api_status()
        add_log('info', 'Проверка статуса API', status)
        return jsonify(status)
    except Exception as e:
        error_msg = f"Ошибка при проверке статуса API: {str(e)}"
        add_log('error', error_msg)
        return jsonify({
            'status': 'error',
            'message': error_msg,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/messages')
def get_messages():
    """Получение списка сообщений"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        messages = avito_api.get_messages(limit=limit, offset=offset)
        add_log('info', f'Получено {len(messages)} сообщений', {'limit': limit, 'offset': offset})
        
        return jsonify({
            'success': True,
            'messages': messages,
            'count': len(messages)
        })
    except Exception as e:
        error_msg = f"Ошибка при получении сообщений: {str(e)}"
        add_log('error', error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/messages/<message_id>')
def get_message(message_id):
    """Получение конкретного сообщения"""
    try:
        message = avito_api.get_message(message_id)
        if message:
            add_log('info', f'Получено сообщение {message_id}')
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            add_log('warning', f'Сообщение {message_id} не найдено')
            return jsonify({
                'success': False,
                'error': 'Сообщение не найдено'
            }), 404
    except Exception as e:
        error_msg = f"Ошибка при получении сообщения {message_id}: {str(e)}"
        add_log('error', error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/chats')
def get_chats():
    """Получение списка чатов"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        chats = avito_api.get_chats(limit=limit, offset=offset)
        add_log('info', f'Получено {len(chats)} чатов', {'limit': limit, 'offset': offset})
        
        return jsonify({
            'success': True,
            'chats': chats,
            'count': len(chats)
        })
    except Exception as e:
        error_msg = f"Ошибка при получении чатов: {str(e)}"
        add_log('error', error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/chats/<chat_id>')
def get_chat(chat_id):
    """Получение информации о чате"""
    try:
        chat = avito_api.get_chat(chat_id)
        if chat:
            add_log('info', f'Получена информация о чате {chat_id}')
            return jsonify({
                'success': True,
                'chat': chat
            })
        else:
            add_log('warning', f'Чат {chat_id} не найден')
            return jsonify({
                'success': False,
                'error': 'Чат не найден'
            }), 404
    except Exception as e:
        error_msg = f"Ошибка при получении чата {chat_id}: {str(e)}"
        add_log('error', error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/send', methods=['POST'])
def send_message():
    """Отправка сообщения"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Данные не предоставлены'
            }), 400
        
        chat_id = data.get('chat_id')
        message = data.get('message')
        attachments = data.get('attachments', [])
        
        if not chat_id or not message:
            return jsonify({
                'success': False,
                'error': 'Необходимы chat_id и message'
            }), 400
        
        result = avito_api.send_message(chat_id, message, attachments)
        
        if result:
            add_log('info', f'Сообщение отправлено в чат {chat_id}', {
                'chat_id': chat_id,
                'message_length': len(message),
                'attachments_count': len(attachments)
            })
            return jsonify({
                'success': True,
                'result': result
            })
        else:
            add_log('error', f'Не удалось отправить сообщение в чат {chat_id}')
            return jsonify({
                'success': False,
                'error': 'Не удалось отправить сообщение'
            }), 500
            
    except Exception as e:
        error_msg = f"Ошибка при отправке сообщения: {str(e)}"
        add_log('error', error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/messages/<message_id>/read', methods=['PUT'])
def mark_as_read(message_id):
    """Отметить сообщение как прочитанное"""
    try:
        success = avito_api.mark_message_as_read(message_id)
        
        if success:
            add_log('info', f'Сообщение {message_id} отмечено как прочитанное')
            return jsonify({
                'success': True,
                'message': 'Сообщение отмечено как прочитанное'
            })
        else:
            add_log('error', f'Не удалось отметить сообщение {message_id} как прочитанное')
            return jsonify({
                'success': False,
                'error': 'Не удалось отметить сообщение как прочитанное'
            }), 500
            
    except Exception as e:
        error_msg = f"Ошибка при отметке сообщения как прочитанного: {str(e)}"
        add_log('error', error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Загрузка файла"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Файл не предоставлен'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Файл не выбран'
            }), 400
        
        # Сохраняем файл временно
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)
        
        # Загружаем в Avito
        attachment_id = avito_api.upload_attachment(file_path)
        
        # Удаляем временный файл
        os.remove(file_path)
        
        if attachment_id:
            add_log('info', f'Файл загружен с ID {attachment_id}', {
                'filename': file.filename,
                'attachment_id': attachment_id
            })
            return jsonify({
                'success': True,
                'attachment_id': attachment_id
            })
        else:
            add_log('error', f'Не удалось загрузить файл {file.filename}')
            return jsonify({
                'success': False,
                'error': 'Не удалось загрузить файл'
            }), 500
            
    except Exception as e:
        error_msg = f"Ошибка при загрузке файла: {str(e)}"
        add_log('error', error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/logs')
def get_logs():
    """Получение логов приложения"""
    try:
        limit = request.args.get('limit', 100, type=int)
        level = request.args.get('level', 'all')
        
        filtered_logs = app_logs
        
        if level != 'all':
            filtered_logs = [log for log in app_logs if log['level'] == level]
        
        # Возвращаем последние записи
        filtered_logs = filtered_logs[-limit:]
        
        return jsonify({
            'success': True,
            'logs': filtered_logs,
            'count': len(filtered_logs)
        })
    except Exception as e:
        error_msg = f"Ошибка при получении логов: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/webhook/avito', methods=['POST'])
def avito_webhook():
    """Обработчик webhook от Avito"""
    try:
        # Получаем данные запроса
        payload = request.get_data(as_text=True)
        signature = request.headers.get('X-Avito-Signature', '')
        
        add_log('info', 'Получен webhook от Avito', {
            'signature_present': bool(signature),
            'payload_length': len(payload)
        })
        
        # Проверяем подпись если она есть
        if signature and avito_api.webhook_secret:
            if not avito_api.verify_webhook_signature(payload, signature):
                add_log('warning', 'Неверная подпись webhook')
                return jsonify({'error': 'Invalid signature'}), 401
        
        # Парсим данные
        try:
            data = json.loads(payload)
            add_log('info', 'Webhook данные успешно обработаны', data)
        except json.JSONDecodeError as e:
            add_log('error', f'Ошибка парсинга JSON: {str(e)}')
            return jsonify({'error': 'Invalid JSON'}), 400
        
        # Обрабатываем различные типы событий
        event_type = data.get('type')
        
        if event_type == 'message':
            # Новое сообщение
            message_data = data.get('data', {})
            add_log('info', f'Получено новое сообщение: {message_data.get("id", "unknown")}')
            
        elif event_type == 'chat':
            # Изменения в чате
            chat_data = data.get('data', {})
            add_log('info', f'Изменения в чате: {chat_data.get("id", "unknown")}')
            
        else:
            add_log('info', f'Неизвестный тип события: {event_type}')
        
        return jsonify({'success': True})
        
    except Exception as e:
        error_msg = f"Ошибка при обработке webhook: {str(e)}"
        add_log('error', error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/webhook/avito', methods=['GET'])
def webhook_verification():
    """Верификация webhook URL"""
    return jsonify({
        'status': 'ok',
        'message': 'Webhook endpoint is active',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Обработчик 404 ошибки"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Обработчик 500 ошибки"""
    add_log('error', f'Внутренняя ошибка сервера: {str(error)}')
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Запуск приложения на {host}:{port}")
    app.run(host=host, port=port, debug=debug)