from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

VERSION = "v1.0.0"  # меняется на v1.1.0 в green

try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except:
    model = None

@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": VERSION})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    x = np.array(data["x"]).reshape(1, -1)
    prediction = model.predict(x).tolist()
    return jsonify({"prediction": prediction, "version": VERSION})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
