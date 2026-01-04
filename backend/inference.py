from backend.ml_model import get_model
from backend.preprocess import preprocess_input


def run_inference(uploaded_file, media_type):

    image = preprocess_input(uploaded_file)
    if image is None:
        return "Error", 0.0, "Invalid image"

    model = get_model()
    results = model(image)

    best = max(results, key=lambda x: x["score"])
    score = float(best["score"])
    label = best["label"].lower()

    if score >= 0.75:
        verdict = "Likely Deepfake" if label == "fake" else "Likely Real"
        explanation = "High confidence prediction"
    elif score >= 0.55:
        verdict = "Inconclusive"
        explanation = "Medium confidence"
    else:
        verdict = "Uncertain"
        explanation = "Low confidence"

    return verdict, score, explanation
