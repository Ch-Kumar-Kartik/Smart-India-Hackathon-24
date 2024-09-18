from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response  # Ensure chat.py is available

app = Flask(__name__)
CORS(app)

@app.route("/")
def index_get():
    return render_template("base.html")

@app.route("/predict", methods=["POST"]) 
def predict():
    text = request.get_json().get("message")
    if not text:
        return jsonify({"error": "Message not provided"}), 400
    response = get_response(text)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True)
