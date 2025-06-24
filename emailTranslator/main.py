import logging
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from emailTranslator.config import Config
from emailTranslator.agent import EmailAgent, EmailData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

subapp = FastAPI()
agent = EmailAgent(api_key=Config.OPENAI_API_KEY, model=Config.DEFAULT_MODEL)


@subapp.post("/email")
async def handle_incoming_email(email: EmailData, request: Request):
    logger.info("Starting email process")
    # logger.info(f"Body length: {len(email.body)}")
    # logger.info(f"Raw email body (first 500 chars): {repr(email.body[:500])}")

    client_ip = request.client.host
    token = request.headers.get("x-api-token")

    if token != Config.API_TOKEN:
        logger.warning(f"Unauthorized access attempt from {client_ip}")
        raise HTTPException(status_code=401, detail="Unauthorized")

    logger.info(
        f"Email received from {email.sender} (IP: {client_ip}) | Subject: {email.subject}"
    )

    if not email.body.strip():
        raise HTTPException(status_code=400, detail="Email body is empty")

    result = agent.process_email_safely(email)

    if result.success:
        agent.send_email(result.summary_email)
        return {"status": "processed"}

    else:
        logger.error(f"Failed to process email from {email.sender}: {result.error}")
        raise HTTPException(status_code=500, detail=result.error)


@subapp.get("/")
def home():
    return {"status": "alive"}

app = FastAPI()
app.mount("/emailTranslator", subapp)


