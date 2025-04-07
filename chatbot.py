

from dotenv import load_dotenv
import streamlit as st
import os
import time
import google.generativeai as genai
from fpdf import FPDF

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyD3E4Cxh1YT-GiB_-sdm_Dxt_KZWICx91A"))

# Gemini setup
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

# Set Streamlit page config
st.set_page_config(page_title="ChatBot", layout="centered")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;600&display=swap');

    html, body, .stApp {
        font-family: 'Figtree', sans-serif;
        background: #f4f6f8;
    }

   

    .title {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 700;
        background: linear-gradient(to right, #7209b7, #f72585);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .message {
        display: flex;
        gap: 12px;
        align-items: flex-start;
        margin-bottom: 20px;
        animation: fadeIn 0.4s ease-in-out;
    }

    .avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
    }

    .bubble {
        background: #eaeaea;
        padding: 12px 16px;
        border-radius: 12px;
        max-width: 85%;
        font-size: 16px;
        line-height: 1.5;
    }

    .user .bubble {
        background: #5e60ce;
        color: white;
        margin-left: auto;
    }

    .user {
        flex-direction: row-reverse;
    }

    .bot .bubble {
        background: #f1f3f5;
        color: #222;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .stTextInput > div > div > input {
        padding: 12px;
        font-size: 16px;
        border-radius: 8px;
    }

    div.stButton > button {
        background: linear-gradient(to right, #7209b7, #f72585);
        color: white;
        font-weight: 600;
        padding: 10px 24px;
        border-radius: 10px;
        border: none;
        margin-top: 10px;
    }

    div.stButton > button:hover {
        background: linear-gradient(to right, #560bad, #d00000);
    }
</style>
""", unsafe_allow_html=True) 

# App container
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="title">🤖 ChatBot</h1>', unsafe_allow_html=True)

# Session state
if "latest_user_input" not in st.session_state:
    st.session_state.latest_user_input = ""
if "latest_bot_response" not in st.session_state:
    st.session_state.latest_bot_response = ""

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask me anything:", placeholder="Type your message...")
    submitted = st.form_submit_button("Send")

# Process input
if submitted and user_input:
    st.session_state.latest_user_input = user_input
    st.session_state.latest_bot_response = ""
    
    response = chat.send_message(user_input, stream=True)

    response_placeholder = st.empty()
    collected = ""

    for chunk in response:
        collected += chunk.text
        response_placeholder.markdown(
            f"""
            <div class="message bot">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" class="avatar"/>
                <div class="bubble">{collected}</div>
            </div>
            """, unsafe_allow_html=True
        )
        time.sleep(0.04)

    st.session_state.latest_bot_response = collected

# Render user message
if st.session_state.latest_user_input:
    st.markdown(f"""
        <div class="message user">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712047.png" class="avatar"/>
            <div class="bubble">{st.session_state.latest_user_input}</div>
        </div>
    """, unsafe_allow_html=True)

# Export to PDF
def export_to_pdf(user_text, bot_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"User: {user_text}\n\nBot: {bot_text}")
    return pdf

if st.session_state.latest_bot_response:
    if st.button("📄 Export to PDF"):
        pdf = export_to_pdf(
            st.session_state.latest_user_input,
            st.session_state.latest_bot_response
        )
        pdf_path = "chat_output.pdf"
        pdf.output(pdf_path)
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="⬇️ Download PDF",
                data=file,
                file_name="chat_response.pdf",
                mime="application/pdf"
            )

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
