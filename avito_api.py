"""
Модуль для работы с API Avito
Обеспечивает получение и отправку сообщений через API Avito
"""

import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AvitoAPI:
    """Класс для работы с API Avito"""
    
    def __init__(self):
        self.client_id = os.getenv('AVITO_CLIENT_ID')
        self.client_secret = os.getenv('AVITO_CLIENT_SECRET')
        self.access_token = os.getenv('AVITO_ACCESS_TOKEN')
        self.webhook_secret = os.getenv('AVITO_WEBHOOK_SECRET')
        
        # Базовые URL для API Avito
        self.base_url = "https://api.avito.ru"
        self.api_version = "v1"
        
        # Проверяем наличие необходимых переменных
        if not all([self.client_id, self.client_secret, self.access_token]):
            logger.error("Не все необходимые переменные окружения установлены")
            raise ValueError("Не все необходимые переменные окружения установлены")
    
    def _get_headers(self) -> Dict[str, str]:
        """Получение заголовков для запросов к API"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Выполнение запроса к API"""
        url = f"{self.base_url}/{self.api_version}/{endpoint}"
        headers = self._get_headers()
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(f"Неподдерживаемый метод: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при выполнении запроса к API: {e}")
            raise
    
    def get_messages(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        Получение списка сообщений
        
        Args:
            limit: Количество сообщений для получения
            offset: Смещение от начала списка
            
        Returns:
            Список сообщений
        """
        try:
            endpoint = f"messages?limit={limit}&offset={offset}"
            response = self._make_request('GET', endpoint)
            
            logger.info(f"Получено {len(response.get('messages', []))} сообщений")
            return response.get('messages', [])
            
        except Exception as e:
            logger.error(f"Ошибка при получении сообщений: {e}")
            return []
    
    def get_message(self, message_id: str) -> Optional[Dict]:
        """
        Получение конкретного сообщения по ID
        
        Args:
            message_id: ID сообщения
            
        Returns:
            Данные сообщения или None
        """
        try:
            endpoint = f"messages/{message_id}"
            response = self._make_request('GET', endpoint)
            
            logger.info(f"Получено сообщение с ID: {message_id}")
            return response
            
        except Exception as e:
            logger.error(f"Ошибка при получении сообщения {message_id}: {e}")
            return None
    
    def send_message(self, chat_id: str, message: str, attachments: Optional[List[str]] = None) -> Optional[Dict]:
        """
        Отправка сообщения
        
        Args:
            chat_id: ID чата
            message: Текст сообщения
            attachments: Список ID вложений (опционально)
            
        Returns:
            Результат отправки или None
        """
        try:
            data = {
                'chat_id': chat_id,
                'message': message
            }
            
            if attachments:
                data['attachments'] = attachments
            
            endpoint = "messages"
            response = self._make_request('POST', endpoint, data)
            
            logger.info(f"Сообщение отправлено в чат {chat_id}")
            return response
            
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            return None
    
    def get_chats(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        Получение списка чатов
        
        Args:
            limit: Количество чатов для получения
            offset: Смещение от начала списка
            
        Returns:
            Список чатов
        """
        try:
            endpoint = f"chats?limit={limit}&offset={offset}"
            response = self._make_request('GET', endpoint)
            
            logger.info(f"Получено {len(response.get('chats', []))} чатов")
            return response.get('chats', [])
            
        except Exception as e:
            logger.error(f"Ошибка при получении чатов: {e}")
            return []
    
    def get_chat(self, chat_id: str) -> Optional[Dict]:
        """
        Получение информации о конкретном чате
        
        Args:
            chat_id: ID чата
            
        Returns:
            Данные чата или None
        """
        try:
            endpoint = f"chats/{chat_id}"
            response = self._make_request('GET', endpoint)
            
            logger.info(f"Получена информация о чате: {chat_id}")
            return response
            
        except Exception as e:
            logger.error(f"Ошибка при получении чата {chat_id}: {e}")
            return None
    
    def mark_message_as_read(self, message_id: str) -> bool:
        """
        Отметить сообщение как прочитанное
        
        Args:
            message_id: ID сообщения
            
        Returns:
            True если успешно, False в противном случае
        """
        try:
            endpoint = f"messages/{message_id}/read"
            self._make_request('PUT', endpoint)
            
            logger.info(f"Сообщение {message_id} отмечено как прочитанное")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при отметке сообщения как прочитанного: {e}")
            return False
    
    def upload_attachment(self, file_path: str) -> Optional[str]:
        """
        Загрузка вложения
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            ID загруженного файла или None
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"Файл не найден: {file_path}")
                return None
            
            endpoint = "attachments"
            url = f"{self.base_url}/{self.api_version}/{endpoint}"
            headers = self._get_headers()
            
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()
                
                result = response.json()
                attachment_id = result.get('id')
                
                logger.info(f"Файл загружен с ID: {attachment_id}")
                return attachment_id
                
        except Exception as e:
            logger.error(f"Ошибка при загрузке файла: {e}")
            return None
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Проверка подписи webhook
        
        Args:
            payload: Тело запроса
            signature: Подпись из заголовка
            
        Returns:
            True если подпись верна, False в противном случае
        """
        try:
            import hmac
            import hashlib
            
            # Создаем подпись
            expected_signature = hmac.new(
                self.webhook_secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception as e:
            logger.error(f"Ошибка при проверке подписи webhook: {e}")
            return False
    
    def get_api_status(self) -> Dict:
        """
        Проверка статуса подключения к API
        
        Returns:
            Словарь со статусом подключения
        """
        try:
            # Пробуем получить список чатов для проверки подключения
            chats = self.get_chats(limit=1)
            
            return {
                'status': 'connected',
                'timestamp': datetime.now().isoformat(),
                'message': 'Подключение к API Avito установлено',
                'chats_count': len(chats)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'message': f'Ошибка подключения к API: {str(e)}',
                'chats_count': 0
            }

# Создаем глобальный экземпляр API
avito_api = AvitoAPI()