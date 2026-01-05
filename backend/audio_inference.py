# backend/audio_inference.py
import tempfile
import os
import traceback
import numpy as np
import librosa
from backend.audio_ml_model import get_audio_model

def run_audio_inference(uploaded_file):
    """
    Read uploaded Flask FileStorage safely, load waveform (mono, 16k),
    send {"array": audio, "sampling_rate": sr} to the HF audio pipeline.
    Returns (verdict, confidence, explanation).
    """

    model = get_audio_model()
    temp_path = None

    try:
        # 1) Save uploaded file to a temp path
        suffix = os.path.splitext(uploaded_file.filename)[1] or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            uploaded_file.save(tmp.name)
            temp_path = tmp.name

        # 2) Use librosa to load audio robustly (handles many formats)
        #    Force sample rate to 16000 and mono.
        audio, sr = librosa.load(temp_path, sr=16000, mono=True)

        # Ensure dtype is float32
        audio = np.asarray(audio, dtype=np.float32)

        # 3) Call the HF audio-classification pipeline with correct input
        results = model({
            "array": audio,
            "sampling_rate": int(sr)
        })

    except Exception as e:
        # Log full traceback for debugging (paste this if it still errors)
        print("Audio inference error:", e)
        traceback.print_exc()
        # Clean up temp file if it exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return "Error", 0.0, "Invalid or unsupported audio file"

    # Clean up temp file
    if temp_path and os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except Exception:
            pass

    # 4) Post-process model output into verdict
    try:
        best = max(results, key=lambda x: x.get("score", 0))
        score = float(best.get("score", 0.0))
        label = best.get("label", "").lower()
    except Exception:
        return "Error", 0.0, "Model returned unexpected output"

    if score >= 0.75:
        verdict = "Likely Deepfake" if label == "fake" else "Likely Real"
        explanation = "High confidence audio classification"
    elif score >= 0.55:
        verdict = "Inconclusive"
        explanation = "Medium confidence audio classification"
    else:
        verdict = "Uncertain"
        explanation = "Low confidence audio classification"

    return verdict, score, explanation
