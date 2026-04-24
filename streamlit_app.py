import streamlit as st
from PIL import Image
import os

from model_pipeline import FoodDetector
from calorie_estimator import CalorieEstimator
from chatbot import NutritionChatbot

# ---------------- CONFIG ----------------
st.set_page_config(page_title="NutriVision AI", layout="wide")

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_models():
    detector = FoodDetector()
    estimator = CalorieEstimator()
    chatbot = NutritionChatbot()
    return detector, estimator, chatbot

detector, estimator, chatbot = load_models()

# ---------------- SESSION ----------------
if "context_data" not in st.session_state:
    st.session_state.context_data = {}

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Upload an image to start analysis!"}
    ]

# ---------------- UI ----------------
st.title("🍽️ NutriVision AI")

col1, col2 = st.columns(2)

# ---------------- IMAGE SECTION ----------------
with col1:
    st.header("📸 Upload Food Image")

    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

        if st.button("Analyze Food"):
            with st.spinner("Analyzing..."):

                results = detector.detect_food(image)

                if not results:
                    st.error("No food detected")
                else:
                    top = results[0]
                    label = top["label"]
                    confidence = float(top["score"])

                    st.success(f"Detected: {label} ({confidence:.2%})")

                    nutrition = estimator.estimate_calories(label)

                    st.session_state.context_data = nutrition

                    st.write("### Nutrition Info")
                    st.json(nutrition)

                    st.session_state.messages = [
                        {"role": "assistant",
                         "content": f"I detected {label}. Ask me anything about it!"}
                    ]

# ---------------- CHAT SECTION ----------------
with col2:
    st.header("💬 Nutrition Chatbot")

    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    prompt = st.chat_input("Ask about food...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = chatbot.generate_response(
                    prompt,
                    st.session_state.context_data
                )
                st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
