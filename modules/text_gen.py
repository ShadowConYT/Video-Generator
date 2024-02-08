import pathlib
import os
from dotenv import load_dotenv
import textwrap
import google.generativeai as genai

load_dotenv()
BARD_API_KEY = os.getenv("BARD_API_KEY")
genai.configure(api_key=BARD_API_KEY)


def text_generation(prompt: str):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    final = textwrap.fill(response.text, width=80)
    return final.replace("**", "").replace("*", "")

