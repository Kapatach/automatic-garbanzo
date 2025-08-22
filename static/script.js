// Глобальные переменные
let currentTab = 'messages';
let uploadedFiles = [];

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Настройка навигации
    setupNavigation();
    
    // Проверка статуса API
    checkApiStatus();
    
    // Загрузка данных для активной вкладки
    loadTabData();
    
    // Настройка формы отправки
    setupSendForm();
    
    // Настройка загрузки файлов
    setupFileUpload();
    
    // Автообновление каждые 30 секунд
    setInterval(autoRefresh, 30000);
}

// Настройка навигации
function setupNavigation() {
    const navTabs = document.querySelectorAll('.nav-tab');
    
    navTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

// Переключение вкладок
function switchTab(tabName) {
    // Убираем активный класс со всех вкладок
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Активируем выбранную вкладку
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
    
    currentTab = tabName;
    loadTabData();
}

// Загрузка данных для активной вкладки
function loadTabData() {
    switch(currentTab) {
        case 'messages':
            loadMessages();
            break;
        case 'chats':
            loadChats();
            break;
        case 'logs':
            loadLogs();
            break;
    }
}

// Проверка статуса API
async function checkApiStatus() {
    const statusIndicator = document.getElementById('statusIndicator');
    const statusDot = statusIndicator.querySelector('.status-dot');
    const statusText = statusIndicator.querySelector('.status-text');
    
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.status === 'connected') {
            statusDot.className = 'status-dot connected';
            statusText.textContent = 'Подключено к API';
        } else {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Ошибка подключения';
        }
    } catch (error) {
        statusDot.className = 'status-dot error';
        statusText.textContent = 'Нет подключения';
        console.error('Ошибка проверки статуса:', error);
    }
}

// Загрузка сообщений
async function loadMessages() {
    const container = document.getElementById('messagesContainer');
    container.innerHTML = '<div class="loading">Загрузка сообщений...</div>';
    
    try {
        const response = await fetch('/api/messages?limit=50');
        const data = await response.json();
        
        if (data.success) {
            displayMessages(data.messages);
        } else {
            container.innerHTML = `<div class="error">Ошибка: ${data.error}</div>`;
        }
    } catch (error) {
        container.innerHTML = '<div class="error">Ошибка загрузки сообщений</div>';
        console.error('Ошибка загрузки сообщений:', error);
    }
}

// Отображение сообщений
function displayMessages(messages) {
    const container = document.getElementById('messagesContainer');
    
    if (messages.length === 0) {
        container.innerHTML = '<div class="empty">Сообщений не найдено</div>';
        return;
    }
    
    const messagesHtml = messages.map(message => `
        <div class="message-card" onclick="showMessageDetails('${message.id}')">
            <div class="message-header">
                <span class="message-sender">${message.sender_name || 'Неизвестный'}</span>
                <span class="message-time">${formatDate(message.created_at)}</span>
            </div>
            <div class="message-text">${message.text || 'Нет текста'}</div>
            <div class="message-actions">
                <button class="btn btn-primary" onclick="event.stopPropagation(); markAsRead('${message.id}')">
                    <i class="fas fa-check"></i> Прочитано
                </button>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = messagesHtml;
}

// Загрузка чатов
async function loadChats() {
    const container = document.getElementById('chatsContainer');
    container.innerHTML = '<div class="loading">Загрузка чатов...</div>';
    
    try {
        const response = await fetch('/api/chats?limit=50');
        const data = await response.json();
        
        if (data.success) {
            displayChats(data.chats);
        } else {
            container.innerHTML = `<div class="error">Ошибка: ${data.error}</div>`;
        }
    } catch (error) {
        container.innerHTML = '<div class="error">Ошибка загрузки чатов</div>';
        console.error('Ошибка загрузки чатов:', error);
    }
}

// Отображение чатов
function displayChats(chats) {
    const container = document.getElementById('chatsContainer');
    
    if (chats.length === 0) {
        container.innerHTML = '<div class="empty">Чатов не найдено</div>';
        return;
    }
    
    const chatsHtml = chats.map(chat => `
        <div class="chat-card" onclick="showChatDetails('${chat.id}')">
            <div class="chat-info">
                <span class="chat-title">${chat.title || 'Без названия'}</span>
                <span class="chat-meta">ID: ${chat.id}</span>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = chatsHtml;
}

// Загрузка логов
async function loadLogs() {
    const container = document.getElementById('logsContainer');
    const level = document.getElementById('logLevel').value;
    
    container.innerHTML = '<div class="loading">Загрузка логов...</div>';
    
    try {
        const response = await fetch(`/api/logs?limit=100&level=${level}`);
        const data = await response.json();
        
        if (data.success) {
            displayLogs(data.logs);
        } else {
            container.innerHTML = `<div class="error">Ошибка: ${data.error}</div>`;
        }
    } catch (error) {
        container.innerHTML = '<div class="error">Ошибка загрузки логов</div>';
        console.error('Ошибка загрузки логов:', error);
    }
}

// Отображение логов
function displayLogs(logs) {
    const container = document.getElementById('logsContainer');
    
    if (logs.length === 0) {
        container.innerHTML = '<div class="empty">Логов не найдено</div>';
        return;
    }
    
    const logsHtml = logs.map(log => `
        <div class="log-item">
            <div>
                <span class="log-timestamp">${formatDate(log.timestamp)}</span>
                <span class="log-level ${log.level}">${log.level.toUpperCase()}</span>
                <span class="log-message">${log.message}</span>
            </div>
            ${log.data ? `<div class="log-data">${JSON.stringify(log.data, null, 2)}</div>` : ''}
        </div>
    `).join('');
    
    container.innerHTML = logsHtml;
}

// Настройка формы отправки
function setupSendForm() {
    const form = document.getElementById('sendForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const chatId = document.getElementById('chatId').value;
        const messageText = document.getElementById('messageText').value;
        
        if (!chatId || !messageText) {
            showNotification('Заполните все обязательные поля', 'error');
            return;
        }
        
        await sendMessage(chatId, messageText);
    });
}

// Отправка сообщения
async function sendMessage(chatId, messageText) {
    try {
        const response = await fetch('/api/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chat_id: chatId,
                message: messageText,
                attachments: uploadedFiles
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Сообщение отправлено успешно', 'success');
            document.getElementById('sendForm').reset();
            uploadedFiles = [];
            updateFileList();
        } else {
            showNotification(`Ошибка отправки: ${data.error}`, 'error');
        }
    } catch (error) {
        showNotification('Ошибка отправки сообщения', 'error');
        console.error('Ошибка отправки:', error);
    }
}

// Настройка загрузки файлов
function setupFileUpload() {
    const fileInput = document.getElementById('fileUpload');
    
    fileInput.addEventListener('change', function(e) {
        const files = Array.from(e.target.files);
        
        files.forEach(file => {
            uploadFile(file);
        });
        
        // Очищаем input
        e.target.value = '';
    });
}

// Загрузка файла
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            uploadedFiles.push(data.attachment_id);
            updateFileList();
            showNotification(`Файл "${file.name}" загружен`, 'success');
        } else {
            showNotification(`Ошибка загрузки файла: ${data.error}`, 'error');
        }
    } catch (error) {
        showNotification('Ошибка загрузки файла', 'error');
        console.error('Ошибка загрузки файла:', error);
    }
}

// Обновление списка файлов
function updateFileList() {
    const fileList = document.getElementById('fileList');
    
    if (uploadedFiles.length === 0) {
        fileList.innerHTML = '<div class="empty">Файлы не выбраны</div>';
        return;
    }
    
    const filesHtml = uploadedFiles.map((fileId, index) => `
        <div class="file-item">
            <span class="file-name">Файл ${index + 1} (ID: ${fileId})</span>
            <span class="file-remove" onclick="removeFile(${index})">×</span>
        </div>
    `).join('');
    
    fileList.innerHTML = filesHtml;
}

// Удаление файла из списка
function removeFile(index) {
    uploadedFiles.splice(index, 1);
    updateFileList();
}

// Отметить сообщение как прочитанное
async function markAsRead(messageId) {
    try {
        const response = await fetch(`/api/messages/${messageId}/read`, {
            method: 'PUT'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Сообщение отмечено как прочитанное', 'success');
            loadMessages(); // Обновляем список
        } else {
            showNotification(`Ошибка: ${data.error}`, 'error');
        }
    } catch (error) {
        showNotification('Ошибка отметки сообщения', 'error');
        console.error('Ошибка отметки:', error);
    }
}

// Показать детали сообщения
async function showMessageDetails(messageId) {
    try {
        const response = await fetch(`/api/messages/${messageId}`);
        const data = await response.json();
        
        if (data.success) {
            showModal('Детали сообщения', formatMessageDetails(data.message));
        } else {
            showNotification(`Ошибка: ${data.error}`, 'error');
        }
    } catch (error) {
        showNotification('Ошибка загрузки деталей', 'error');
        console.error('Ошибка загрузки деталей:', error);
    }
}

// Показать детали чата
async function showChatDetails(chatId) {
    try {
        const response = await fetch(`/api/chats/${chatId}`);
        const data = await response.json();
        
        if (data.success) {
            showModal('Детали чата', formatChatDetails(data.chat));
        } else {
            showNotification(`Ошибка: ${data.error}`, 'error');
        }
    } catch (error) {
        showNotification('Ошибка загрузки деталей чата', 'error');
        console.error('Ошибка загрузки деталей чата:', error);
    }
}

// Форматирование деталей сообщения
function formatMessageDetails(message) {
    return `
        <div class="message-details">
            <p><strong>ID:</strong> ${message.id}</p>
            <p><strong>Отправитель:</strong> ${message.sender_name || 'Неизвестный'}</p>
            <p><strong>Время:</strong> ${formatDate(message.created_at)}</p>
            <p><strong>Текст:</strong></p>
            <div class="message-text-content">${message.text || 'Нет текста'}</div>
            ${message.attachments && message.attachments.length > 0 ? 
                `<p><strong>Вложения:</strong> ${message.attachments.length}</p>` : ''}
        </div>
    `;
}

// Форматирование деталей чата
function formatChatDetails(chat) {
    return `
        <div class="chat-details">
            <p><strong>ID:</strong> ${chat.id}</p>
            <p><strong>Название:</strong> ${chat.title || 'Без названия'}</p>
            <p><strong>Создан:</strong> ${formatDate(chat.created_at)}</p>
            <p><strong>Обновлен:</strong> ${formatDate(chat.updated_at)}</p>
        </div>
    `;
}

// Показать модальное окно
function showModal(title, content) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalBody').innerHTML = content;
    document.getElementById('modal').classList.add('active');
}

// Закрыть модальное окно
function closeModal() {
    document.getElementById('modal').classList.remove('active');
}

// Показать уведомление
function showNotification(message, type = 'info') {
    const notifications = document.getElementById('notifications');
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notifications.appendChild(notification);
    
    // Автоматически удаляем через 5 секунд
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Форматирование даты
function formatDate(dateString) {
    if (!dateString) return 'Неизвестно';
    
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Автообновление
function autoRefresh() {
    if (currentTab === 'messages' || currentTab === 'chats' || currentTab === 'logs') {
        loadTabData();
    }
}

// Закрытие модального окна по клику вне его
document.addEventListener('click', function(e) {
    const modal = document.getElementById('modal');
    if (e.target === modal) {
        closeModal();
    }
});

// Закрытие модального окна по Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});