from openai import OpenAI
from pydantic import BaseModel
import logging
from typing import List, Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from emailTranslator.config import Config

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


# Email data =================================================
class EmailData(BaseModel):
    sender: str
    date: str
    subject: str
    body: str


class TranslatedEmail(BaseModel):
    translated_subject: str
    translated_body: str
    languages_detected: List[str]


class ProcessedEmail(BaseModel):
    original_sender: str
    actionable: bool
    action: Optional[str] = None
    who: Optional[str] = None
    summary: List[str]


class SummaryEmail(BaseModel):
    subject: str
    body: str


class SafeguardResult(BaseModel):
    email_pass: bool
    reason: str
    threat_type: Optional[str] = None


class ProcessingResult(BaseModel):
    success: bool
    processed_email: Optional[ProcessedEmail] = None
    summary_email: Optional[SummaryEmail] = None
    error: Optional[str] = None
    threat_type: Optional[str] = None


# Agent =====================================================
class EmailAgent:
    """
    Process flow:
        1) Check email is safe
        2)
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        max_email_length: int = 10000,
        max_subject_length: int = 500,
    ):
        logger.info("Starting Email Agent")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        # Length limits configuration
        self.max_email_length = max_email_length
        self.max_subject_length = max_subject_length

    def run_safeguards(self, email: EmailData) -> SafeguardResult:
        """
        Check email length limits to prevent processing issues.
        Returns SafeguardResult indicating if email is safe to process.
        """
        # Check email length limits
        total_length = len(email.subject) + len(email.body)

        logger.info(
            f"Checking email length: subject={len(email.subject)}, body={len(email.body)}, total={total_length}"
        )

        if total_length > self.max_email_length:
            logger.warning(
                f"Email rejected: too long ({total_length} chars > {self.max_email_length})"
            )
            return SafeguardResult(
                email_pass=False,
                reason=f"Email too long: {total_length} characters exceeds limit of {self.max_email_length}",
                threat_type="length_limit",
            )

        if len(email.subject) > self.max_subject_length:
            logger.warning(
                f"Email rejected: subject too long ({len(email.subject)} chars)"
            )
            return SafeguardResult(
                email_pass=False,
                reason=f"Subject too long: {len(email.subject)} characters exceeds limit of {self.max_subject_length}",
                threat_type="length_limit",
            )

        logger.info("Email passed length checks")
        return SafeguardResult(email_pass=True, reason="Email passed length checks")

    def check_email_language(self, email: EmailData) -> TranslatedEmail:
        """
        See if email contains any other languages like Portuguese.
        """
        logger.info("Checking email language")

        system_prompt = """ 
        You are a professional translator. You will be given data from an email. 
        You will be given either an email subject and body. This will
        be indicated in the string by 'Subject' or 'Body'.
        You need to check whether the language of the subject and body 
        is all written in English or not.
        If the email is all or partially in another language, like Portuguese, 
        translate everything into English (UK not USA). 
        
        Make sure not to translate things like people's names, place names, email 
        addresses from the
        original language. Make a decision about which parts of the email data
        are appropriate to translate.
        
        Return the data in the original format but with appropriate translations.
        If the original data was all English just 
        return the original data. Also return a list of the languages detected.
        """

        # LLM cant take in a list of subject, body: needs one string
        email_str = f"Subject: {email.subject}\n\nBody: {email.body}"

        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": email_str,
                    },
                ],
                response_format=TranslatedEmail,
            )

            results = completion.choices[0].message.parsed

        except Exception as e:
            logger.error("Language check LLM call failed", exc_info=True)
            raise

        logger.info("Email language checked and translated.")

        # Return as TranslatedEmail Pydantic model
        return TranslatedEmail(
            translated_subject=results.translated_subject,
            translated_body=results.translated_body,
            languages_detected=results.languages_detected,
        )

    def summarise_email(self, email: TranslatedEmail) -> ProcessedEmail:
        """
        Bullet points summary of email with possible actions.
        """
        logger.info("Summarising email")

        system_prompt = """
            Your job is to take in an email or chain of emails and provide
            a short and concise summary. You will receive the email subject and 
            email body denoted in the string by 'Subject' and 'Body'. In addition
            you need to figure out if any actions are required, what the actions 
            are and who may need to carry out the actions. You also need to figure 
            out who the first sender from the body text. The email is being 
            forwarded from my account so the 'sender' field is my email 
            but the 'original_sender' will be the first email after 'From'.

            If in doubt for any results return None. 
            
            Return the summary as a list of bullet points (e.g. ["Point 1", "Point 2"]). 
            Do not format it as a paragraph.

            """

        # LLM cant take in a list of subject, body: needs one string
        email_str = (
            f"Subject: {email.translated_subject}\n\nBody: {email.translated_body}"
        )

        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": email_str,
                    },
                ],
                response_format=ProcessedEmail,
            )

            results = completion.choices[0].message.parsed

        except Exception as e:
            logger.error("Summary LLM call failed", exc_info=True)
            raise

        logger.info("Email summarised")

        return ProcessedEmail(
            original_sender=results.original_sender,
            summary=results.summary,
            actionable=results.actionable,
            action=results.action,
            who=results.who,
        )

    def write_summary_email(
        self, processed: ProcessedEmail, translated: TranslatedEmail
    ) -> SummaryEmail:
        """
        Final format of summary email.
        """
        summary_bullets = "\n".join(f"- {point}" for point in processed.summary)

        # Email content
        subject = f"Summary of: {translated.translated_subject}"

        body = f"""
        Hello, 

        Sender: {processed.original_sender}

        Summary:

        {summary_bullets}

        Any actions: {processed.actionable}
        Actions: {processed.action or "None"}

        Full translation:

        {translated.translated_body}

        From DM
        """

        return SummaryEmail(subject=subject, body=body)

    def process_email_safely(self, email: EmailData) -> ProcessingResult:
        """
        Main method to process email with length checks.
        Returns ProcessingResult with either processed email or error information.
        """

        # Run length checks first
        safeguard_result = self.run_safeguards(email)

        if not safeguard_result.email_pass:
            logger.error(f"Email processing blocked: {safeguard_result.reason}")

            return ProcessingResult(
                success=False,
                error=safeguard_result.reason,
                threat_type=safeguard_result.threat_type,
            )

        try:
            # Process email normally if it passes length checks
            translated_email = self.check_email_language(email)
            processed_email = self.summarise_email(translated_email)
            summary_email = self.write_summary_email(processed_email, translated_email)

            return ProcessingResult(
                success=True,
                processed_email=processed_email,
                summary_email=summary_email,
            )

        except Exception as e:
            logger.error(f"Error processing email: {str(e)}", exc_info=True)

            return ProcessingResult(
                success=False,
                error=f"Processing failed: {str(e)}",
                threat_type="processing_error",
            )

    def send_email(self, summary_email: SummaryEmail, to_email: str = None):
        """
        Send email based on setup in Config file. Expects subject and
        body to be pre-processed i.e. will send exactly as it.
        """
        logger.info("Sending summary email")

        subject = summary_email.subject
        body = summary_email.body

        # Option to send to other email
        SEND_TO = to_email or Config.DEFAULT_RECIPIENT

        # Create MIME structure
        msg = MIMEMultipart()
        msg["From"] = Config.EMAIL_USERNAME
        msg["To"] = SEND_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send email via SMTP
        SMPT_SERVER = Config.SMTP_SERVER
        SMPT_PORT = Config.SMTP_PORT

        try:
            with smtplib.SMTP_SSL(SMPT_SERVER, SMPT_PORT) as server:
                server.login(Config.EMAIL_USERNAME, Config.EMAIL_PASSWORD)
                server.send_message(msg)

            logger.info("Summary email sent")

        except Exception as e:
            logger.error(f"Language check LLM call failed, {e}", exc_info=True)


if __name__ == "__main__":
    from emailTranslator.config import Config
    from emailTranslator.emails import load_example_email

    email = load_example_email(5)
    email = EmailData(**email)

    agent = EmailAgent(api_key=Config.OPENAI_API_KEY, model=Config.DEFAULT_MODEL)

    # Use the new safe processing method
    result = agent.process_email_safely(email)

    if result.success:
        print("Email processed successfully!")
        print(result.model_dump_json(indent=2))
        agent.send_email(summary_email=result.summary_email)

    else:
        print(f"Email processing failed: {result.error}")
        print(f"Threat type: {result.threat_type or 'Unknown'}")
