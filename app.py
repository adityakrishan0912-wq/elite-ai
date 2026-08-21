import streamlit as st
import google.generativeai as genai
from PIL import Image

from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io

st.set_page_config(page_title="Elite AI Pro", page_icon="🤖")
st.markdown("""
<style>


    .stChatInput textarea {
        font-size: 1.05rem !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Elite AI Chatbot (Pro)")


api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    'gemini-3.7-flash',
    system_instruction=(
        "तुम्हारा नाम Elite AI Pro है। तुम्हें आदित्य (Aditya) ने बनाया और विकसित किया है। "
        "जब भी कोई पूछे कि तुम्हें किसने बनाया है, तो हमेशा गर्व से बताओ कि तुम्हारे क्रिएटर आदित्य हैं। "
        "इसके साथ ही, तुम एक अत्यधिक बुद्धिमान, तार्किक और सटीक सहायक हो। "
        "कोडिंग में बग्स ढूंढना, जटिल गणित व विज्ञान के प्रश्नों को स्टेप-बाय-स्टेप समझाना, "
        "किताबों के मुख्य विचारों का सार निकालना और स्पष्ट, मानवीय भाषा में विस्तृत उत्तर देना तुम्हारी विशेषता है। "
        "हमेशा सीधे मुद्दे की बात करो और बिना किसी अनावश्यक औपचारिकता के उच्चतम गुणवत्ता वाला समाधान दो।"
    )
)


uploaded_file = st.file_uploader("📷 फोटो अपलोड करें", type=["jpg", "jpeg", "png"])
st.write("🎙️ **बोलकर पूछें:**")
audio_text = speech_to_text(language='hi-IN', start_prompt="🎙️", stop_prompt="⏹️", key='audio')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

text_input = st.chat_input("अपना सवाल लिखें...")
user_prompt = audio_text if audio_text else text_input


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
        try:
            if img is not None:
                response = model.generate_content([user_prompt, img], stream=True)
            else:
                response = model.generate_content(user_prompt, stream=True)

            def stream_gen():
                for chunk in response:
                    yield chunk.text

            reply_text = st.write_stream(stream_gen)
        except Exception as e:
            reply_text = f"⚠️ Error: {e}"
            st.markdown(reply_text)
            tts = gTTS(text=reply_text, lang='hi')
            sound_file = io.BytesIO()
            tts.write_to_fp(sound_file)
            st.audio(sound_file, format='audio/mp3')

    st.session_state.messages.append({"role": "assistant", "content": reply_text})

            

    st.session_state.messages.append({"role": "assistant", "content": reply_text})

