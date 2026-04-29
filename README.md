# ChatBot-LobiFind — Asistente Virtual con IA

Aplicación web desarrollada con Python, Flask y la API de OpenAI. Funciona como un 
asistente chatbot que responde preguntas frecuentes sobre el uso de LobiFind, 
plataforma de asesorías universitarias en pares de la UTSJR.

> 💡 Proyecto personal propuesto como módulo complementario para LobiFind.

---

## ✨ Funcionalidades

- Interfaz de chat inspirada en apps de mensajería (estilo WhatsApp/Messenger).
- Responde preguntas frecuentes sobre el funcionamiento de LobiFind.
- Mantiene el historial de la conversación durante la sesión.
- Indicador de "escribiendo..." en tiempo real.
- Interacción dinámica sin recargar la página, usando peticiones `fetch`.

---

## 🛠️ Tecnologías utilizadas

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **IA:** API de OpenAI (gpt-4o-mini)

---

## ✅ Requisitos previos

- Python 3.8 o superior instalado.
- Una clave API de OpenAI válida.

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/rakerito/ChatBot-LobiFind.git
cd ChatBot-LobiFind
```

### 2. Crear y activar un entorno virtual *(recomendado)*

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto y agrega tu clave API:

### 5. Ejecutar la aplicación

```bash
python app.py
```

### 6. Abrir en el navegador

Ve a [http://localhost:5000](http://localhost:5000) y comienza a conversar.

---

## 👩‍💻 Autora

**Raquel Pastor Gaytán**  
[github.com/rakerito](https://github.com/rakerito)
