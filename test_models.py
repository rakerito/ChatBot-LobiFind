import os
import requests
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("GEMINI_API_KEY")

try:
    resp = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={key}")
    data = resp.json()
    
    if resp.status_code != 200:
        print(f"Error HTTP {resp.status_code}: {data}")
    else:
        models = [m['name'] for m in data.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
        print("Modelos disponibles:")
        print(models)
except Exception as e:
    print(f"Error de conexión: {e}")
