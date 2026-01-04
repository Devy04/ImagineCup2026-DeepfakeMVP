from PIL import Image

def preprocess_input(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        return image.convert("RGB")
    except Exception:
        return None
