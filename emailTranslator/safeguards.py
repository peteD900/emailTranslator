# emailTranslator/safeguards.py

from emailTranslator.logger import get_logger
from emailTranslator.models import EmailData, SafeguardResult
from emailTranslator.config import Config

logger = get_logger()


class SafeGuarder:
    """
    Performs all safety and loop checks on incoming emails before processing.

    Args:
        max_email_length (int): Limit for total email size.
        max_subject_length (int): Limit for subject length.
    """

    def __init__(self):
        logger.info("Starting SafeGuarder")
        self.max_email_length = Config.MAX_EMAIL_LENGTH

    def is_loop_email(self, email: EmailData) -> bool:
        """
        Check if the email appears to be from our own system or a forwarding loop.
        """
        if email.headers:
            loop_headers = [
                "X-Email-Translator-Processed",
                "X-Loop",
                "X-Forwarded-By-EmailTranslator",
                "X-Auto-Response-Suppress",
            ]
            for header in loop_headers:
                if header in email.headers:
                    logger.warning(f"Loop detected via header: {header}")
                    return True

        if "Summary of:" in email.subject:
            if email.subject.count("Summary of:") >= 2:
                logger.warning("Nested summary detected")
                return True

        subject_lower = email.subject.lower()
        auto_reply_subjects = [
            "auto-reply",
            "automatic reply",
            "out of office",
            "ooo",
            "away message",
            "vacation reply",
            "delivery status notification",
            "undelivered mail",
            "mail delivery failed",
            "returned mail",
            "delivery failure",
            "bounce",
            "mailer-daemon",
        ]
        if any(indicator in subject_lower for indicator in auto_reply_subjects):
            logger.warning("Auto-reply detected in subject")
            return True

        body_lower = email.body.lower()
        auto_reply_body_patterns = [
            "this is an automated response",
            "automatic reply",
            "out of office",
            "i am currently away",
            "delivery status notification",
            "undelivered mail returned to sender",
            "mail delivery failed",
            "message could not be delivered",
        ]
        if any(pattern in body_lower for pattern in auto_reply_body_patterns):
            logger.warning("Auto-reply detected in body")
            return True

        sender_lower = email.sender.lower()
        system_senders = [
            "noreply",
            "no-reply",
            "mailer-daemon",
            "postmaster",
            "bounce",
            "delivery",
            "automated",
            "system",
        ]
        if any(system_sender in sender_lower for system_sender in system_senders):
            logger.warning(f"System sender detected: {email.sender}")
            return True

        if "From DM" in email.body:
            logger.warning("Detected our own forwarded email signature")
            return True

        return False

    def email_too_long(self, email: EmailData) -> bool:
        subject_length = len(email.subject)
        body_length = len(email.body)
        total_length = subject_length + body_length
        self.email_length = total_length

        logger.info(
            f"Checking email length: subject={subject_length}, body={body_length}, total = {total_length}"
        )

        return total_length > self.max_email_length

    def run(self, email: EmailData) -> SafeguardResult:
        """
        Runs all configured safety checks on the given email. At the moment checks are:
         - Detect if email is stuck in a forwarding loop
         - Check email length isn't too big
        """

        if self.is_loop_email(email):
            return SafeguardResult(
                email_pass=False,
                reason="Email appears to be part of a forwarding loop or auto-reply",
                threat_type="loop_detected",
            )

        if self.email_too_long(email):
            return SafeguardResult(
                email_pass=False,
                reason=f"Email too long: {self.email_length} characters exceeds limit of {self.max_email_length}",
                threat_type="length_limit",
            )

        # if nothing fails above email is ok
        email_ok = SafeguardResult(
            email_pass=True, reason="Email passed all safety checks"
        )

        return email_ok


if __name__ == "__main__":
    from emailTranslator.emailer import load_example_email

    email = load_example_email(3)
    guard = EmailSafeguard()

    # should pass all
    guard.is_loop_email(email)
    guard.email_too_long(email)
    guard.run(email)

    # should fail length check
    email.body = email.body * 100
    guard.run(email)

    # should fail headers
    guard.run(load_example_email(0))
