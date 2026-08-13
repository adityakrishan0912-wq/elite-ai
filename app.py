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
model = genai.GenerativeModel('gemini-1.5-flash')
uploaded_file = st.file_uploader("📷 फोटो अपलोड करें", type=["jpg", "jpeg", "png"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("अपना सवाल लिखें..."):
    img = None
    if uploaded_file:
        img = Image.open(uploaded_file)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        if img:
            st.image(img, width=200)
        st.markdown(prompt)
    with st.chat_message("assistant"):
        if img:
            response = model.generate_content([prompt, img])
        else:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        st.markdown(response.text)

