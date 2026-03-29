# Asistente de Soporte para Inventario y Ventas

Aplicación web creada con Python, Flask y la API de OpenAI. Funciona como un asistente chatbot que ayuda a los usuarios a entender cómo usar un sistema de inventario.

## Funcionalidades
- Frontend con estilo de aplicación de mensajería (WhatsApp/Messenger).
- Mantiene el historial de la conversación.
- Indicador de "escribiendo..." en tiempo real.
- Interacción en la misma vista usando peticiones `fetch`.
- Prompt de sistema configurado para actuar como experto en control de inventario y ventas.

## Requisitos previos
- Python 3.8+ instalado.
- Una Clave API de OpenAI válida.

## Instalación y ejecución

1. **Clonar/Abrir el directorio del proyecto**
   Asegúrate de estar en el directorio `ChatBot`.

2. **Crear y activar un entorno virtual (Opcional pero recomendado)**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Variables de entorno (.env)**
   Crea un archivo llamado `.env` en el directorio raíz del proyecto y agrega tu clave API de OpenAI:
   ```env
   OPENAI_API_KEY=tu-clave-api-aqui
   ```
   **Nota respecto a los modelos de OpenAI**: Dentro de la solicitud se pidió usar el nombre `gpt-4.1-mini`. En caso de que recibas un mensaje de error indicando que dicho modelo no existe por parte de la API, entra al archivo `app.py` y modifícalo por el modelo en uso real actualmente: `gpt-4o-mini` o `gpt-3.5-turbo`.

5. **Ejecutar la aplicación (Backend de Flask)**
   ```bash
   python app.py
   ```

6. **Abrir en el navegador**
   Ve a [http://127.0.0.1:5000](http://127.0.0.1:5000) o [http://localhost:5000](http://localhost:5000) y comienza a conversar.
