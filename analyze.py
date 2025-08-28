import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please add it to .env")
genai.configure(api_key=api_key)

def analyze_with_gemini(code, filename):
    prompt = f"""
    You are a malware code analyst.
    Analyze this source code from {filename}.
    1. What does the code do?
    2. Which lines are suspicious or malicious? (include line numbers if possible)
    3. What MITRE ATT&CK techniques apply?
    Code:
    {code}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
