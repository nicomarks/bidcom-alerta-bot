import httpx
import time
import re
import json

# --- CONFIG ---
URL = "https://www.bidcom.com.ar/outlet"
PALABRAS = ["dji", "gopro"]
ENVIADOS = set()

INSTANCE_ID = "instance154139"
TOKEN = "fpt30690oq2sq4k0"
NUMERO = "+543513214333"

def enviar_whatsapp(mensaje):
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    data = {
        "token": TOKEN,
        "to": NUMERO,
        "body": mensaje
    }
    try:
        httpx.post(url, data=data)
        print("Mensaje enviado a WhatsApp.")
    except Exception as e:
        print("Error enviando mensaje:", e)

def obtener_html():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "*/*",
    }
    try:
        r = httpx.get(URL, headers=headers, follow_redirects=True, timeout=20)
        return r.text
    except Exception as e:
        print("Error al obtener HTML:", e)
        return None

def buscar_productos(html):
    productos = []
    pattern = r'<a class="productItemTitle".*?>(.*?)<\/a>'
    matches = re.findall(pattern, html, re.DOTALL)

    for m in matches:
        nombre = re.sub("<.*?>", "", m).strip()
        productos.append(nombre.lower())

    return productos

def loop():
    print("Bot ejecutándose en Render...")

    while True:
        html = obtener_html()
        if html:
            productos = buscar_productos(html)

            for p in productos:
                for palabra in PALABRAS:
                    if palabra in p and p not in ENVIADOS:
                        ENVIADOS.add(p)
                        enviar_whatsapp(f"¡NUEVO PRODUCTO! 🔥\nCoincidencia: {p}")
                        print("Coincidencia:", p)

        time.sleep(60)  # chequea cada 1 minuto

if __name__ == "__main__":
    loop()


