from transformers import pipeline
_audio_detector = pipeline(
    "audio-classification",
    model="MelodyMachine/Deepfake-audio-detection-V2"
)

def get_audio_model():
    return _audio_detector
