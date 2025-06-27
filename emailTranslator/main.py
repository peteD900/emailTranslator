from fastapi import FastAPI, Request, HTTPException
from emailTranslator.summariser import Summariser
from emailTranslator.emailer import Emailer
from emailTranslator.logger import get_logger
from emailTranslator.models import EmailData
from emailTranslator.config import Config


logger = get_logger()

subapp = FastAPI()
summariser = Summariser()
emailer = Emailer()


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

    result = summariser.process_email(email)

    if result.success:
        emailer.send_email(result.final_email)
        return {"status": "processed"}

    else:
        logger.error(f"Failed to process email from {email.sender}: {result.error}")
        raise HTTPException(status_code=500, detail=result.error)


@subapp.get("/")
def home():
    return {"status": "alive"}


app = FastAPI()
app.mount("/emailTranslator", subapp)
