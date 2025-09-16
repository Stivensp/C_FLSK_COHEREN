from flask import Flask, render_template, jsonify
import cohere
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

app = Flask(__name__, static_folder="static")

COHERE_API_KEY = "LtpNmUJdnTSDl4HW06g7KUitLN9tg3P9HxjmNoJf"
co = cohere.Client(COHERE_API_KEY)

def get_clipboard_text():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    text = clipboard.wait_for_text()
    return text if text else ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analizar", methods=["GET"])
def analizar():
    try:
        texto = get_clipboard_text()
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
