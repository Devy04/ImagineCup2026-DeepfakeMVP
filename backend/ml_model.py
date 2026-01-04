from transformers import pipeline

_detector = pipeline(
    "image-classification",
    model="dima806/deepfake_vs_real_image_detection"
)

def get_model():
    return _detector
