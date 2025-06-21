from pyprojroot import here
import json
import os


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
    return email


if __name__ == "__main__":
    # examples
    email = load_example_email(3)
    print(email)

    # test send
    send_email(subject="test from pete", body="this is a test")
