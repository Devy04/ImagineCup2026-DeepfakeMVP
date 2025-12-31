from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/detect", methods=["POST"])
def detect():
    media_type = request.form.get("media_type")
    uploaded_file = request.files.get("file")

    if uploaded_file is None or media_type is None:
        return jsonify({
            "error": "Missing file or media type"
        }), 400

   
    # dummy logic

    verdict = "Likely Deepfake"
    confidence = 0.82
    explanation = "Detected spectral inconsistencies"

    return jsonify({
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
