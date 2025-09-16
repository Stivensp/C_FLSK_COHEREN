from flask import Flask, jsonify
import cohere
import pyperclip

app = Flask(__name__)

COHERE_API_KEY = "LtpNmUJdnTSDl4HW06g7KUitLN9tg3P9HxjmNoJf"
co = cohere.Client(COHERE_API_KEY)

@app.route("/")
def home():
    return "✅ Servidor con portapapeles + Cohere activo"

@app.route("/analizar", methods=["GET"])
def analizar():
    try:
        texto = pyperclip.paste()
    except Exception as e:
        return jsonify({"respuesta": f"Error accediendo al portapapeles: {e}"})

    if not texto.strip():
        return jsonify({"respuesta": "No hay texto en el portapapeles"})

    response = co.chat(
        model="command-xlarge-nightly",
        message=texto + " solamente la respuesta correcta lo más resumido posible"
    )

    return jsonify({"respuesta": response.text})

if __name__ == "__main__":
    app.run(debug=True, port=5500)
