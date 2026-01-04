from flask import request, jsonify
from backend.inference import run_inference
def register_routes(app):
    @app.route("/detect", methods=["POST"])
    def detect():
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        verdict, confidence, explanation = run_inference(file, "image")

        return jsonify({
            "verdict": verdict,
            "confidence": confidence,
            "explanation": explanation
        })
