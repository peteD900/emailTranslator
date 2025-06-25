# Data models
from pydantic import BaseModel
from typing import List, Optional


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


class SafeguardResult(BaseModel):
    """
    Used in pre-checks before processing email with LLM.
     - Output of run_safeguards() in safeguards.py
    """

    email_pass: bool
    reason: str
    threat_type: Optional[str] = None


class TranslatedEmail(BaseModel):
    """
    - Model response for check_email_language()
    - Input to summarise_email() and write_summary_email()

    """

    translated_subject: str
    translated_body: str
    languages_detected: List[str]


class ProcessedEmail(BaseModel):
    """
    The stuff I actually want to extract from the original email.

     - Model reponse for summarise_email()
     - Input to write_summary_email()
    """

    original_sender: str
    actionable: bool
    action: Optional[str] = None
    who: Optional[str] = None
    summary: List[str]  #


class SummaryEmail(BaseModel):
    """
    For sending out results.

     - Output of write_summary_email()
    """

    subject: str
    body: str


class ProcessingResult(BaseModel):
    """
    Final result of the process. Contains all the info required to
    write and send summmary email.
     - Input to
     - Output of process_email_safely()

    """

    success: bool
    processed_email: Optional[ProcessedEmail] = None
    summary_email: Optional[SummaryEmail] = None
    error: Optional[str] = None
    threat_type: Optional[str] = None
