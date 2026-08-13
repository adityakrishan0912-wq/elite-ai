
Elite AI Assistant
-------------------
A single-file Streamlit web app powered by Google Gemini.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

Deploy:
    - Streamlit Cloud: push app.py + requirements.txt to a repo, set GOOGLE_API_KEY in Secrets.
    - Hugging Face Spaces: create a "Streamlit" Space, upload these two files,
      add GOOGLE_API_KEY as a Space secret.
"""

import base64
import time

import streamlit as st
import google.generativeai as genai

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Elite | Advanced AI Solutions",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# BRAND COLORS
# --------------------------------------------------------------------------
NAVY = "#0F172A"
NAVY_LIGHT = "#1E293B"
GOLD = "#D4AF37"
GOLD_SOFT = "#F1D98B"
TEXT_LIGHT = "#E5E7EB"

# --------------------------------------------------------------------------
# INLINE BASE64 LOGO (self-contained gold diamond "E" mark — no external file needed)
# Replace this SVG string with your own logo markup if you have a custom asset.
# --------------------------------------------------------------------------
LOGO_SVG = """
<svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F1D98B"/>
      <stop offset="50%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#9C7A1E"/>
    </linearGradient>
  </defs>
  <polygon points="36,2 70,36 36,70 2,36" fill="none" stroke="url(#g)" stroke-width="3"/>
  <text x="36" y="46" font-family="Georgia, serif" font-size="30" font-weight="bold"
        text-anchor="middle" fill="url(#g)">E</text>
</svg>
"""
LOGO_B64 = base64.b64encode(LOGO_SVG.encode("utf-8")).decode("utf-8")
LOGO_DATA_URI = f"data:image/svg+xml;base64,{LOGO_B64}"

# --------------------------------------------------------------------------
# GLOBAL CSS — dark navy + metallic gold theme
# --------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {NAVY};
        color: {TEXT_LIGHT};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {NAVY_LIGHT};
        border-right: 1px solid {GOLD};
    }}
    #MainMenu, footer {{visibility: hidden;}}

    /* Header */
    .elite-header {{
        text-align: center;
        padding: 1.2rem 0 0.5rem 0;
    }}
    .elite-title {{
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, {GOLD_SOFT}, {GOLD}, #9C7A1E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.3rem 0 0.1rem 0;
        letter-spacing: 2px;
    }}
    .elite-subtitle {{
        color: #94A3B8;
        font-size: 0.95rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }}
    hr.gold-divider {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {GOLD}, transparent);
        margin: 0.5rem 0 1.2rem 0;
    }}

    /* Chat bubbles */
    .chat-row {{
        display: flex;
        margin-bottom: 12px;
    }}
    .chat-row.user {{ justify-content: flex-end; }}
    .chat-row.assistant {{ justify-content: flex-start; }}

    .bubble {{
        max-width: 78%;
        padding: 12px 16px;
        border-radius: 16px;
        line-height: 1.5;
        font-size: 0.96rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.35);
    }}
    .bubble.user {{
        background: linear-gradient(135deg, {GOLD}, #B8912C);
        color: #0F172A;
        border-bottom-right-radius: 4px;
        font-weight: 500;
    }}
    .bubble.assistant {{
        background: {NAVY_LIGHT};
        color: {TEXT_LIGHT};
        border: 1px solid rgba(212,175,55,0.35);
        border-bottom-left-radius: 4px;
    }}
    .bubble-label {{
        font-size: 0.7rem;
        opacity: 0.7;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Buttons */
    div.stButton > button {{
        background-color: transparent;
        color: {GOLD};
        border: 1px solid {GOLD};
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        width: 100%;
    }}
    div.stButton > button:hover {{
        background-color: {GOLD};
        color: {NAVY};
        border-color: {GOLD};
    }}
    div.stButton > button:focus {{
        box-shadow: 
