import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Elite AI", page_icon="🤖")
st.title("🤖 Elite AI Chatbot")

# Sidebar में API Key का इनपुट
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

if not api_key:
    st.info("👈 पहले Sidebar में अपनी Google Gemini API Key डालें।")
    st.stop()

# Gemini Config
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Elite AI से कुछ भी पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}"


