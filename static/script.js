document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');

    const sessionId = Math.random().toString(36).substring(2, 15);

    messageInput.addEventListener('input', () => {
        sendButton.disabled = messageInput.value.trim() === '';
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        
        messageInput.value = '';
        sendButton.disabled = true;
        
        showTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    mensaje: message,
                    session_id: sessionId
                })
            });

            const data = await response.json();
            
            hideTypingIndicator();

            if (response.ok) {
                addMessage(data.respuesta, 'bot');
            } else {
                addMessage(`Error: ${data.error || 'Ocurrió un problema en el servidor'}`, 'bot', true);
            }
        } catch (error) {
            hideTypingIndicator();
            addMessage('Error de conexión con el servidor.', 'bot', true);
        }
    });

    function addMessage(text, sender, isError = false) {
        // En lugar de hacer scroll automático siempre, verificamos si el usuario estaba cerca del fondo.
        // Si el usuario scrolleó hacia arriba para leer historia, NO lo forzamos abajo (estilo WhatsApp).
        const isNearBottom = chatMessages.scrollHeight - chatMessages.scrollTop <= chatMessages.clientHeight + 150;
        
        const stickerRegex = /\[STICKER:([a-zA-Z0-9_]+)\]/g;
        const stickers = [];
        
        // Remover las etiquetas de sticker del texto principal y guardarlas
        const cleanText = text.replace(stickerRegex, (match, name) => {
            stickers.push(name);
            return ''; 
        }).trim();

        // 1. Manda absolutamente todo el texto en una sola burbuja primero
        if (cleanText) {
            renderBubble(cleanText, sender, isError, false);
        }
        
        // 2. Manda todos los stickers descubiertos después, como burbujas separadas al estilo WhatsApp
        stickers.forEach((stickerName) => {
            renderBubble(stickerName, sender, false, true);
        });

        // Solo bajamos si el usuario es el que envió, O si ya estaba abajo visualizando recientes.
        if (sender === 'user' || isNearBottom) {
            // Un pequeño timeout para asegurar que el DOM pintó las imágenes o su tamaño
            setTimeout(scrollToBottom, 50);
        }
    }

    function renderBubble(content, sender, isError, isSticker) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message ${isError ? 'error-message' : ''}`;
        
        const contentDiv = document.createElement('div');
        
        if (isSticker) {
            contentDiv.className = 'sticker-content'; // Clase sin burbuja blanca
            contentDiv.innerHTML = `<img src="/static/stickers/${content}.png" class="chat-sticker" alt="Sticker ${content}">`;
        } else {
            contentDiv.className = 'message-content'; // Clase de texto normal
            let formattedText = escapeHTML(content);
            formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            formattedText = formattedText.replace(/\n/g, '<br>');
            contentDiv.innerHTML = formattedText;
        }
        
        messageDiv.appendChild(contentDiv);
        chatMessages.insertBefore(messageDiv, typingIndicator);
    }

    function showTypingIndicator() {
        const isNearBottom = chatMessages.scrollHeight - chatMessages.scrollTop <= chatMessages.clientHeight + 150;
        typingIndicator.classList.remove('hidden');
        if (isNearBottom) {
            scrollToBottom();
        }
    }

    function hideTypingIndicator() {
        typingIndicator.classList.add('hidden');
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }
});
