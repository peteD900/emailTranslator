import requests
from datetime import datetime
from emailTranslator.config import Config


API_URL = "http://127.0.0.1:8000/emailTranslator/email"
API_TOKEN = Config.API_TOKEN

email_data = {
    "sender": "test@example.com",
    "date": "2025-06-08T09:15:00",
    "subject": "Testing the Summariser",
    "body": "Hi, this is a test email to check local processing before VPS deploy!",
}

headers = {"x-api-token": API_TOKEN, "Content-Type": "application/json"}

response = requests.post(API_URL, json=email_data, headers=headers)

print("Status Code:", response.status_code)
print("Headers:", response.headers)

# Show raw response text if not JSON
try:
    print("JSON Response:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Raw Response:", response.text)
