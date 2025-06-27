# Main summarising functions
from emailTranslator.logger import get_logger
from emailTranslator.llm import get_llm_client
from emailTranslator.safeguards import SafeGuarder
from emailTranslator.models import (
    EmailData,
    LanguageCheck,
    TranslatedText,
    TranslatedEmail,
    SummarisedEmail,
    FinalEmail,
    ProcessingResult,
)

logger = get_logger()


class Summariser:
    def __init__(self):
        logger.info("Starting Summariser")
        self.llm = get_llm_client()
        self.guard = SafeGuarder()

    def check_email_language(self, email: EmailData) -> LanguageCheck:
        """
        Checks to see if email is not in English and needs translating.
        """
        logger.info("Checking email language")

        system_prompt = """
        Your job is to check the language of some text taken from an email. You will 
        be given the first 100 words. If you detect that the text is not English then
        you will return that the email needs to be translated. Also return what language was 
        detected even if it just English. Some English emails may contain a handful of non-English
        words and you have to make a call on whether the majority of the text is an 
        another language.
        """

        # Save tokens by just passing the head.
        # If this is unstable maybe sample parts of the full chain.
        email_head = email.body[0:100]

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": email_head,
            },
        ]

        result = self.llm.parse_completion(
            messages=messages, response_format=LanguageCheck
        )

        return result

    def translate_text(self, txt=str) -> str:
        """
        Translates email body and subject to English.
        """

        logger.info("Translating text")

        system_prompt = """ 
        You are a professional translator. You will be given some text, usually
        taken from an email subject or body to translate into English.

        Make sure not to translate things like people's names, place names, email 
        addresses from the
        original language. Make a decision about which parts of the text
        are appropriate to translate.
        
        Return the text in the original format as well as you can.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": txt,
            },
        ]

        result = self.llm.parse_completion(
            messages=messages, response_format=TranslatedText
        )

        return result

    def translate_email(
        self, email: EmailData, needs_translating: bool
    ) -> TranslatedEmail:
        """
        If required translated subject and body into English. Else return the
        orginal text
        """
        if needs_translating:
            translated_subject = self.translate_text(email.subject)
            translated_body = self.translate_text(email.body)

        else:
            translated_subject = email.subject
            translated_body = email.body

        return TranslatedEmail(
            translated_subject=str(translated_subject),
            translated_body=str(translated_body),
        )

    def summarise_email(self, email: TranslatedEmail) -> SummarisedEmail:
        """
        Bullet points summary of email with possible actions.
        """
        logger.info("Summarising email")

        system_prompt = """
            You are a personal email summary assistant for me. Your goal is
            to summarise my personal emails and let me know if I need to do 
            anthing. 

            Your job is to take in an email or chain of emails and provide
            a short and concise summary in the form of a list (bullet points).     

            Be sparing with the number of list entries, the idea is to sum
            up the context of the email and any highlight anything actionalable, 
            urgent, or informative. I do not need to know descriptive aspects 
            like 'It will be fun' or 'it's a celebration'. I just need to know,
            for example, what is happening, when, do I need to do anything.

            You need to figure out if any actions are required, what the actions 
            are and if I personally need to do anything. If no actions return None.
            
            Return the summary as a list of bullet points (e.g. ["Point 1", "Point 2"]). 
            Do not format it as a paragraph.
            """

        # LLM cant take in a list of subject, body: needs one string
        email_str = (
            f"Subject: {email.translated_subject}\n\nBody: {email.translated_body}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": email_str,
            },
        ]

        result = self.llm.parse_completion(
            messages=messages, response_format=SummarisedEmail
        )

        logger.info("Email summarised")

        return result

    def write_summary_email(
        self, translation: TranslatedEmail, summary: SummarisedEmail
    ) -> FinalEmail:
        """
        Final format of summary email with loop prevention.
        """
        summary_bullets = "\n".join(f"- {point}" for point in summary.summary)

        subject = translation.translated_subject

        body = f"""
        Hello, 

        Summary:

        {summary_bullets}

        Any actions: {summary.actionable}
        Actions: {summary.action or "None"}

        Full translation:

        {translation.translated_body}

        From Dave Mason        

        """

        return FinalEmail(subject=subject, body=body)

    def process_email(self, email: EmailData) -> SummarisedEmail:
        """
        Checks language and translated if required.
        """
        logger.info("Processing email")

        # Run all safety checks first (including loop detection)
        safeguard_result = self.guard.run(email)

        if not safeguard_result.email_pass:
            logger.error(f"Email processing blocked: {safeguard_result.reason}")

            return ProcessingResult(
                success=False,
                error=safeguard_result.reason,
                threat_type=safeguard_result.threat_type,
            )

        # If safeguards pass them move onto processing:
        try:
            # Translate
            language_check = self.check_email_language(email)
            translation = self.translate_email(email, language_check.needs_translating)

            # Summarise
            summarised_email = self.summarise_email(translation)

            # Write final email
            final_email = self.write_summary_email(translation, summarised_email)

            return ProcessingResult(
                success=True,
                final_email=final_email,
            )

        except Exception as e:
            logger.error(f"Error processing email: {str(e)}", exc_info=True)

            return ProcessingResult(
                success=False,
                error=f"Processing failed: {str(e)}",
                threat_type="processing_error",
            )


if __name__ == "__main__":
    from emailer import load_example_email

    email = load_example_email(3)

    summariser = Summariser()

    # Needs translation?
    # print(summariser.check_email_language(email))

    # Full summary
    summary = summariser.process_email(email)
    if summary.success:
        print(summary.model_dump_json(indent=2))
        print(summary.final_email.body)
