import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    # LLM
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")

    # email
    SMTP_SERVER = "smtp.mailo.com"
    SMTP_PORT = 465
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    DEFAULT_RECIPIENT = os.getenv("EMAIL_TO")

    # api
    API_TOKEN = os.getenv("API_TOKEN")
