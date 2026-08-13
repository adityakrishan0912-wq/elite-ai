import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Elite AI Pro", page_icon="🤖")
st.title("🤖 Elite AI Chatbot (Pro)")

api_key = st.sidebar.text_input("Google Gemini API Key", type="password")
if not api_key:
    st.info("👈 Sidebar में API Key डालें।")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-3.6-flash")

uploaded_file = st.file_uploader("📷 फोटो अपलोड करें", type=["jpg", "jpeg", "png"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("अपना सवाल लिखें...")

if user_prompt:
    img = None
    if uploaded_file is not None:
        img = Image.open(uploaded_file)

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        if img is not None:
            st.image(img, width=200)
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("सोच रहा हूँ..."):
            try:
                if img is not None:
                    response = model.generate_content([user_prompt, img])
                else:
                    response = model.generate_content(user_prompt)
                reply_text = response.text
            except Exception as e:
                reply_text = f"⚠️ Error: {e}"

        st.markdown(reply_text)

    st.session_state.messages.append({"role": "assistant", "content": reply_text})

