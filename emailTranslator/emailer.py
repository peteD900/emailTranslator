from pyprojroot import here
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from emailTranslator.models import EmailData, SummaryEmail
from emailTranslator.logger import get_logger
from emailTranslator.config import Config

logger = get_logger()


# Send email ========================================================
class Emailer:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        logger.info("Starting Emailer")
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, summary_email: SummaryEmail, send_to):
        """
        Send email with loop prevention headers.
        """
        logger.info("Sending summary email with loop prevention headers")

        subject = summary_email.subject
        body = summary_email.body

        # Create MIME structure
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = send_to
        msg["Subject"] = subject

        # ADD LOOP PREVENTION HEADERS
        msg["X-Email-Translator-Processed"] = "true"
        msg["X-Forwarded-By-EmailTranslator"] = "v1.0"
        msg["X-Auto-Response-Suppress"] = "All"  # Suppress auto-replies
        msg["Precedence"] = "bulk"  # Indicates automated email
        msg["Auto-Submitted"] = "auto-generated"  # RFC 3834 compliant

        msg.attach(MIMEText(body, "plain"))

        # Send email via SMTP
        SMPT_SERVER = self.smtp_server
        SMPT_PORT = self.smtp_port

        try:
            with smtplib.SMTP_SSL(SMPT_SERVER, SMPT_PORT) as server:
                server.login(self.username, self.password)
                server.send_message(msg)

            logger.info(f"Summary email sent successfully to {send_to}")

        except Exception as e:
            logger.error(f"Failed to send email: {e}", exc_info=True)
            raise


# Example emails =====================================================
def load_example_emails():
    """
    Loads example email data for testing agent.
    """

    DATA_PATH = here("data")

    with open(os.path.join(DATA_PATH, "example_emails.json"), "r") as f:
        return json.load(f)


def load_example_email(email_index: int):
    """
    Load a specific example email by index 0-n. See
    data/example_emails.json
    """

    emails = load_example_emails()
    email = emails[email_index]
    email = EmailData(**email)
    return email


if __name__ == "__main__":
    # examples
    email = load_example_email(3)
    print(email)

    # Send email
    email = SummaryEmail(subject="test send", body="this is a test from Pete")
    emailer = Emailer(
        smtp_port=Config.SMTP_PORT,
        smtp_server=Config.SMTP_SERVER,
        username=Config.EMAIL_USERNAME,
        password=Config.EMAIL_PASSWORD,
    )
    emailer.send_email(email, send_to=Config.DEFAULT_RECIPIENT)
