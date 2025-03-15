#!/usr/bin/env python

with open('static/css/floating-notification.css', 'w') as f:
    f.write("""/* Estilos para o ícone de notificação */
.notification-icon {
    position: relative;
    display: inline-block;
}

.notification-badge {
    position: absolute;
    top: -5px;
    right: -5px;
    background-color: #dc3545;
    color: white;
    border-radius: 50%;
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
    min-width: 1rem;
    text-align: center;
}

.notification-dropdown {
    min-width: 300px;
    max-height: 400px;
    overflow-y: auto;
}

.notification-item {
    padding: 0.5rem 1rem;
    border-bottom: 1px solid #eee;
    cursor: pointer;
}

.notification-item:hover {
    background-color: #f8f9fa;
}

.notification-item.unread {
    background-color: #e9f5ff;
}

.notification-item .notification-time {
    font-size: 0.75rem;
    color: #6c757d;
}

.notification-item .notification-message {
    margin-bottom: 0.25rem;
}

.notification-empty {
    padding: 1rem;
    text-align: center;
    color: #6c757d;
}

.notification-footer {
    padding: 0.5rem 1rem;
    text-align: center;
    border-top: 1px solid #eee;
}""") 