import streamlit as st
from PyPDF2 import PdfReader
import openai
import os

# --- Configuration ---
openai.api_key = st.secrets.get("OPENAI_API_KEY")

# --- Functions ---
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def get_resume_feedback(resume_text):
    prompt = f"""
    You are an expert resume reviewer.
    Analyze the following resume text and provide suggestions to:
    1. Improve formatting for ATS
    2. Add missing critical sections if any
    3. Suggest better keyword usage
    4. General tone and clarity improvements

    Resume:
    {resume_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error fetching suggestions: {str(e)}"

# --- Streamlit UI ---
st.set_page_config(page_title="AI Resume Checker", page_icon="📄")
st.title("📄 AI-Powered Resume Checker")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting and analyzing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        st.subheader("Extracted Resume Text")
        st.text_area("Preview", resume_text, height=300)

        st.subheader("🔍 AI Suggestions")
        suggestions = get_resume_feedback(resume_text)
        st.markdown(suggestions)
else:
    st.info("Please upload a PDF resume to begin.")
