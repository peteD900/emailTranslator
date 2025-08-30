import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    # LLM OPENAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-5"

    # MAILO
    MAILO_SMTP_SERVER = "smtp.mailo.com"
    MAILO_SMTP_PORT = 465
    MAILO_USERNAME = os.getenv("EMAIL_USERNAME")
    MAILO_PASSWORD = os.getenv("EMAIL_PASSWORD")

    # SEND TO
    DEFAULT_RECIPIENT = os.getenv("EMAIL_TO")

    # APP API
    API_TOKEN = os.getenv("API_TOKEN")

    # SAFEGAURDS
    MAX_EMAIL_LENGTH = 50000
