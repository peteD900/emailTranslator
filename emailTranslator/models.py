# Data models
from pydantic import BaseModel
from typing import List, Optional


# Main input to process ============================================
class EmailData(BaseModel):
    """
    Format required for pushing email into the agent. Headers are to
    detect forwarding loop.
     - Input to process_email_safely() in agent.py
    """

    sender: str
    date: str
    subject: str
    body: str
    headers: Optional[dict] = None


# safeguards.py ====================================================
class SafeguardResult(BaseModel):
    """
    Used in pre-checks before processing email with LLM.
     - Output of run_safeguards() in safeguards.py
    """

    email_pass: bool
    reason: str
    threat_type: Optional[str] = None


# summariser.py ======================================================
class LanguageCheck(BaseModel):
    """
    Let's system know whether the email needs translating into English.
    """

    needs_translating: bool
    language_detected: str


class TranslatedText(BaseModel):
    translation: str


class TranslatedEmail(BaseModel):
    """
    Format for tranalated email but this is used for emails that were
    not translated also. This is to make futher processing easier.
    """

    translated_subject: str
    translated_body: str


class SummarisedEmail(BaseModel):
    """
    The stuff I actually want to extract from the original email.

     - Model reponse for summarise_email()
     - Input to write_summary_email()
    """

    actionable: bool
    action: Optional[str] = None
    summary: List[str]


class FinalEmail(BaseModel):
    """
    For sending out results.

     - Output of write_summary_email()
    """

    subject: str
    body: str


class ProcessingResult(BaseModel):
    success: bool
    final_email: Optional[FinalEmail] = None
    error: Optional[str] = None
    threat_type: Optional[str] = None


# emailer.py ======================================================
