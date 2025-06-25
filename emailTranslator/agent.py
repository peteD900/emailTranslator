from openai import OpenAI
import logging

from emailTranslator.config import Config
import uuid

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


# Agent =====================================================
class EmailAgent:
    """
    Process flow:
        1) Check email is safe and not a loop
        2) Check language and translate if needed
        3) Summarize email
        4) Send summary with loop prevention headers
    """

    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        logger.info("Starting Email Agent")
        self.client = OpenAI(api_key=api_key)
        self.model = model

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
        Final format of summary email with loop prevention.
        """
        summary_bullets = "\n".join(f"- {point}" for point in processed.summary)

        # Prevent nested "Summary of:" in subject
        original_subject = translated.translated_subject
        if original_subject.startswith("Summary of:"):
            # Don't add another "Summary of:" if it's already a summary
            subject = f"Re-summary: {original_subject}"
        else:
            subject = f"Summary of: {original_subject}"

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
        
        --
        This is an automated email summary. Do not reply to this message.
        System ID: {self.system_id}
        """

        return SummaryEmail(subject=subject, body=body)

    def process_email_safely(self, email: EmailData) -> ProcessingResult:
        """
        Main method to process email with safety checks including loop detection.
        Returns ProcessingResult with either processed email or error information.
        """

        # Run all safety checks first (including loop detection)
        safeguard_result = self.run_safeguards(email)

        if not safeguard_result.email_pass:
            logger.error(f"Email processing blocked: {safeguard_result.reason}")

            return ProcessingResult(
                success=False,
                error=safeguard_result.reason,
                threat_type=safeguard_result.threat_type,
            )

        try:
            # Process email normally if it passes all safety checks
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


if __name__ == "__main__":
    from emailTranslator.config import Config
    from emailTranslator.emailer import load_example_email

    email = load_example_email(3)
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
