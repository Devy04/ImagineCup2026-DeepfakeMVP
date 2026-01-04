from transformers import pipeline
from PIL import Image

# Load deepfake detection model
detector = pipeline(
    "image-classification",
    model="dima806/deepfake_vs_real_image_detection"
)

# Path to your local image
image_path = "backend/test.jpg"   # <-- Enter your image path here

# Open the image
img = Image.open(image_path)

# Predict
results = detector(img)

# Get highest score
best = max(results, key=lambda x: x['score'])

print(f"\nFinal Result: {best['label']} ({best['score']:.4f})")