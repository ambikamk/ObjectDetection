import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import tempfile

# Configure Gemini API
api_key = 'AIzaSyAEpxEaoSLL6Z6gBM3Ha0edMAECjW6h61g'
genai.configure(api_key=api_key)

# Set up the model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(image, prompt):
    response = model.generate_content([prompt, image])
    return response.text

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# Streamlit app - Modern UI
st.markdown("""
    <style>
        /* Set background image */
        body {
            background-image: url('https://your-background-image-url.com');
            background-size: cover;
            background-repeat: no-repeat;
        }
        /* Centralized title styling */
        .stApp {
            background-color: rgba(255, 255, 255, 0.7);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.2);
        }
        h1 {
            color: #FF6347;
            text-align: center;
            font-family: 'Arial Black', Gadget, sans-serif;
        }
        /* Upload button style */
        .stFileUploader {
            margin-top: 2rem;
            text-align: center;
        }
        /* Button Styling */
        button {
            background-color: #FF6347;
            color: white;
            font-size: 1.2rem;
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            margin-top: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #FF4500;
        }
        /* Subheader styling */
        h2 {
            color: #FF6347;
            font-family: 'Arial', sans-serif;
            margin-top: 2rem;
        }
        /* Textbox styling */
        .stText {
            font-family: 'Helvetica', sans-serif;
            font-size: 1.1rem;
            color: #333;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌟 Object Detection and Explanation App 🌟")

uploaded_file = st.file_uploader("📷 Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    if st.button('🔍 Analyze Image'):
        # Detect objects
        detection_prompt = "Identify the main objects in this image."
        detection_result = get_gemini_response(image, detection_prompt)
        
        st.subheader("📋 Detected Objects:")
        st.write(detection_result)
        
        # Get explanation
        explanation_prompt = f"Explain the main object detected in this image: {detection_result}"
        explanation = get_gemini_response(image, explanation_prompt)
        
        st.subheader("📝 Explanation:")
        st.write(explanation)
        
        # Generate audio explanation
        audio_file = text_to_speech(explanation)
        
        # Display audio player
        st.subheader("🎧 Audio Explanation:")
        st.audio(audio_file)
        
        # Clean up the temporary audio file
        os.unlink(audio_file)
