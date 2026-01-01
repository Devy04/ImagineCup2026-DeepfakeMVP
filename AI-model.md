To create a full-fledged, ready-to-execute AI model for detecting if an image is AI-generated (fake) or real, I've used a pre-trained Vision Transformer (ViT) model from Hugging Face: dima806/ai_vs_real_image_detection. This model was fine-tuned on a dataset of real and AI-generated images, achieving 98.25% accuracy on a test set of 48,000 images (balanced classes: precision/recall/F1 ~0.98 for both real and fake). It's based on Google's ViT-base-patch16-224-in21k, with 85.8 million parameters.
This is deployed as a simple web app using Streamlit, allowing users to upload images and get instant predictions with confidence scores. No training is needed—the model loads pre-trained weights automatically.
Setup Instructions

Install dependencies (run in terminal; assumes Python 3.8+):textpip install streamlit transformers torch pillow
Save the code below as ai_image_detector_app.py.
Launch: Run streamlit run ai_image_detector_app.py in terminal. It opens a local web app in your browser (e.g., http://localhost:8501).
Usage: Upload an image (JPEG/PNG), click "Detect", and view the result.

The app handles preprocessing, inference, and output. It runs on CPU by default but uses GPU if available (via PyTorch). For production, deploy on Streamlit Sharing or a server (e.g., Heroku/AWS), but this is ready for local execution and launch.
Pythonimport streamlit as st
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image
import io

# Load the pre-trained model and processor from Hugging Face
@st.cache_resource  # Cache to avoid reloading on every run
def load_model():
    processor = AutoImageProcessor.from_pretrained("dima806/ai_vs_real_image_detection")
    model = AutoModelForImageClassification.from_pretrained("dima806/ai_vs_real_image_detection")
    model.eval()  # Set to evaluation mode
    return processor, model

processor, model = load_model()

# Streamlit app layout
st.title("AI-Generated Image Detector")
st.markdown("""
Upload an image to check if it's real or AI-generated (fake).  
This uses a pre-trained ViT model with ~98% accuracy on balanced datasets.  
Supports JPEG and PNG formats.
""")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Detect button
    if st.button("Detect"):
        with st.spinner("Analyzing..."):
            # Preprocess the image
            inputs = processor(images=image, return_tensors="pt")
            
            # Run inference
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=-1).squeeze().cpu().numpy()
            
            # Model labels: index 0 = REAL, 1 = FAKE (based on Hugging Face config)
            real_prob = probs[0]
            fake_prob = probs[1]
            predicted_class = "Fake (AI-Generated)" if fake_prob > real_prob else "Real"
            confidence = max(real_prob, fake_prob)
            
            # Display results
            st.subheader("Detection Result")
            st.write(f"**Predicted:** {predicted_class}")
            st.write(f"**Confidence:** {confidence:.2%}")
            st.write(f"Real Probability: {real_prob:.2%}")
            st.write(f"Fake Probability: {fake_prob:.2%}")
            
            if confidence < 0.7:
                st.warning("Low confidence—results may vary with image quality or unseen AI generators.")
else:
    st.info("Upload an image to start.")
