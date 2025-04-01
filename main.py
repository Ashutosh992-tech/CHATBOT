import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd
from gtts import gTTS
from io import BytesIO
import base64

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API Key not found! Please set it in a .env file.")
    st.stop()

# Configure Google Generative AI with API Key
genai.configure(api_key=API_KEY)

def ask_hackathon_bot(user_query):
    """Ask the AI chatbot about hackathon-related queries."""
    prompt = (
        f"You are an expert hackathon assistant. Answer the following query accurately:\n\n"
        f"User Query: {user_query}\n\n"
        f"Provide detailed, helpful responses based on common hackathon rules, judging criteria, team requirements, and prizes."
    )
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def text_to_speech(text, lang="en"):
    """Convert text response to speech."""
    tts = gTTS(text=text, lang=lang)
    fp = BytesIO()
    tts.write_to_fp(fp)
    return fp

def convert_csv_to_excel(csv_file):
    df = pd.read_csv(csv_file)
    excel_path = "converted_output.xlsx"
    df.to_excel(excel_path, index=False)
    return excel_path

def convert_excel_to_csv(excel_file):
    df = pd.read_excel(excel_file)
    csv_path = "converted_output.csv"
    df.to_csv(csv_path, index=False)
    return csv_path

def main():
    st.title("🤖 AI Chatbot for Hackathon Queries 🎯")
    st.subheader("Ask me anything about hackathons!")
    
    user_query = st.text_input("Enter your question:")
    if user_query:
        response = ask_hackathon_bot(user_query)
        st.write("🤖 AI Response:", response)
        
        if st.button("🔊 Convert Response to Speech"):
            speech_fp = text_to_speech(response, lang="en")
            st.audio(speech_fp, format="audio/mpeg", start_time=0)
            
            b64 = base64.b64encode(speech_fp.getvalue()).decode()
            st.markdown(f'<a href="data:audio/mpeg;base64,{b64}" download="speech.mp3">📥 Download Audio</a>', unsafe_allow_html=True)
    
    st.sidebar.header("📂 File Conversions")
    csv_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
    if csv_file and st.sidebar.button("Convert CSV to Excel"):
        excel_path = convert_csv_to_excel(csv_file)
        with open(excel_path, "rb") as file:
            st.sidebar.download_button("📥 Download Excel", file, "converted_output.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    excel_file = st.sidebar.file_uploader("Upload an Excel file", type="xlsx")
    if excel_file and st.sidebar.button("Convert Excel to CSV"):
        csv_path = convert_excel_to_csv(excel_file)
        with open(csv_path, "rb") as file:
            st.sidebar.download_button("📥 Download CSV", file, "converted_output.csv", "text/csv")

if __name__ == "__main__":
    main()
