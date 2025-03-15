#!/usr/bin/env python

with open('static/js/notifications.js', 'w') as f:
    f.write("""// Arquivo para gerenciar notificações
document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando sistema de notificações...');
    
    // Função para atualizar o contador de notificações
    function updateNotificationCount() {
        fetch('/dashboard/realtime/unread-count/')
            .then(response => response.json())
            .then(data => {
                const count = data.count;
                const badge = document.getElementById('notification-badge');
                if (badge) {
                    badge.textContent = count;
                    badge.style.display = count > 0 ? 'inline-block' : 'none';
                }
            })
            .catch(error => console.error('Erro ao buscar contagem de notificações:', error));
    }
    
    // Inicializar WebSocket para notificações em tempo real
    function initWebSocket() {
        const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const wsUrl = `${wsScheme}://${window.location.host}/ws/notifications/`;
        
        console.log('Conectando ao WebSocket de notificações:', wsUrl);
        
        try {
            const socket = new WebSocket(wsUrl);
            
            socket.onopen = function(e) {
                console.log('WebSocket de notificações conectado!');
            };
            
            socket.onmessage = function(e) {
                console.log('Mensagem recebida:', e.data);
                try {
                    const data = JSON.parse(e.data);
                    if (data.type === 'notification') {
                        // Atualizar contador de notificações
                        updateNotificationCount();
                    }
                } catch (error) {
                    console.error('Erro ao processar mensagem:', error);
                }
            };
            
            socket.onclose = function(e) {
                console.log('WebSocket de notificações fechado. Código:', e.code, 'Razão:', e.reason);
                setTimeout(initWebSocket, 5000);
            };
            
            socket.onerror = function(e) {
                console.error('Erro no WebSocket de notificações:', e);
            };
            
            return socket;
        } catch (error) {
            console.error('Erro ao criar WebSocket de notificações:', error);
            setTimeout(initWebSocket, 5000);
            return null;
        }
    }
    
    // Inicializar
    updateNotificationCount();
    const socket = initWebSocket();
    
    // Atualizar contador a cada 30 segundos
    setInterval(updateNotificationCount, 30000);
});""") 