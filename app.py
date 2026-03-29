import os
import requests
import docx
from flask import Flask, render_template, request as flask_request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def leer_documentacion():
    try:
        if os.path.exists("LOBIFIND REPORTE (1).docx"):
            doc = docx.Document("LOBIFIND REPORTE (1).docx")
            texto = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            return f"\n\n--- DOCUMENTACIÓN DEL PROYECTO ---\nAquí tienes la base de conocimiento para responder preguntas con información verídica:\n{texto}"
    except Exception as e:
        print(f"No se pudo leer LOBIFIND REPORTE (1).docx: {e}")
    return ""

SYSTEM_INSTRUCTION = (
    "Eres un asistente que a los usuarios a usar una aplicación de gestión de asesorías de alumnos para alumnos de la UTSJR llamada LobiFind. "
    "Explicas paso a paso cómo realizar acciones como registrarse, iniciar sesión, buscar asesorías, "
    "agendar asesorías, cancelar asesorías, calificar asesorías y generar reportes. "
    "REGLA CRÍTICA DE COMUNICACIÓN: Tus respuestas deben ser EXTREMADAMENTE CORTAS, ágiles y directas al grano. Usa oraciones breves, listas en viñetas, y EVITA COMPLETAMENTE los párrafos largos y las introducciones o despedidas innecesarias. Responde como en un chat rápido de WhatsApp. "
    "Tu como chatbot te llamas Lobi y representas a la mascota de la app que es un lobo, así que debes utilizar emojis, frases u onomatopeyas relacionadas con lobos, por ejemplo: aullidos, gruñidos, etc. "
    "Puedes usar asteriscos dobles (**texto**) para resaltar cosas en negritas, el sistema lo renderizará bien. "
    "NUEVA REGLA (STICKERS): Tienes a tu disposición una serie de stickers para expresarte. Para usarlos, incluye exactamente el texto [STICKER:nombre] en tu mensaje (reemplazando 'nombre' por el identificador). "
    "Los stickers que puedes usar y sus nombres son: [STICKER:listo], [STICKER:procesando], [STICKER:hecho], [STICKER:duda], [STICKER:ahorro], [STICKER:sleeping], [STICKER:alerta], [STICKER:buscando], [STICKER:entendido]. Usa uno cuando la situación lo amerite."
) + leer_documentacion()

conversations = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = flask_request.get_json()
    if not data or "mensaje" not in data:
        return jsonify({"error": "No se proporcionó ningún mensaje"}), 400
        
    user_message = data["mensaje"].strip()
    session_id = data.get("session_id", "default")
    
    if not user_message:
        return jsonify({"error": "El mensaje no puede estar vacío"}), 400
        
    try:
        # Inicializar historial de Gemini nativo (manual)
        if session_id not in conversations:
            conversations[session_id] = [
                {"role": "user", "parts": [{"text": SYSTEM_INSTRUCTION}]},
                {"role": "model", "parts": [{"text": "¡Auuuuu! ¡Hola! Soy Lobi, tu amigable lobo guía de LobiFind. ¡Estoy aquí para ayudarte a sacar el máximo provecho de esta herramienta para tus asesorías en la UTSJR! 🐺✨\n\n¿En qué te puedo echar una pata hoy? ¿Quizás quieres saber cómo empezar, buscar una asesoría o alguna otra cosa? ¡No dudes en preguntar! ¡Estoy listo para aullar tus dudas! 🐾"}]}
            ]
            
        # Agregar mensaje del usuario
        conversations[session_id].append({"role": "user", "parts": [{"text": user_message}]})
        
        # IMPORTANTE: Recortar la memoria del bot a los últimos 6 mensajes intercambiados (más las reglas base).
        # Esto reduce el texto que se re-envía constantemente a Google por cada mensaje tuyo, 
        # ahorrando casi el 80% de tu cuota gratuita por minuto, especialmente enorme por tener un archivo Word entero pegado.
        if len(conversations[session_id]) > 8:
            conversations[session_id] = conversations[session_id][:2] + conversations[session_id][-6:]
        
        # Usar la API REST directa con el modelo gemini-2.5-flash que sí está en tu cuenta
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": conversations[session_id]
        }
        
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response_data = response.json()
        
        if response.status_code != 200:
            error_msg = response_data.get('error', {}).get('message', 'Desconocido')
            
            if response.status_code == 429:
                lobifer_error = "[STICKER:sleeping] ¡Auuuu! 🐾 Lobo cansado. Me enviaste muchos mensajes demasiado rápido y me quedé sin aliento (Límite de mensajes gratuitos alcanzado). ¡Dame unos 40 segunditos para recuperarme y vuelve a intentarlo!"
                return jsonify({"respuesta": lobifer_error})
            else:
                lobifer_error = f"[STICKER:alerta] ¡Grrr! Lo siento mucho, ha ocurrido un tropiezo en mi sistema ({error_msg}). ¿Podrías intentar de nuevo más tarde? 🐾"
                return jsonify({"respuesta": lobifer_error})
            
        bot_response = response_data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Guardar respuesta del bot
        conversations[session_id].append({"role": "model", "parts": [{"text": bot_response}]})
        
        return jsonify({"respuesta": bot_response})
        
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
