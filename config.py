from dotenv import load_dotenv
import os

load_dotenv()

MODEL = os.getenv("MODEL", "gemini-2.5-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")