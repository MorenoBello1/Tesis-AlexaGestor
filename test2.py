import os
import requests
import json
import base64

# Obtén la clave API de la variable de entorno
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# URL del endpoint de la API
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro-vision-001:generateContent?key={GOOGLE_API_KEY}"

# Encabezados para la solicitud
headers = {
    'Content-Type': 'application/json',
}

# Leer la imagen y codificarla en base64
with open("ruta/a/tu/imagen.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Datos (payload) para ser enviados en la solicitud POST
data = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "inlineData": {
                        "mimeType": "image/png",
                        "data": encoded_image
                    }
                },
                {
                    "text": "Describe this picture."
                }
            ]
        }
    ]
}

# Convertir el payload a JSON
data_json = json.dumps(data)

# Realizar la solicitud POST
response = requests.post(url, headers=headers, data=data_json)

# Verificar la respuesta
if response.status_code == 200:
    print("Respuesta de la API:", response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)