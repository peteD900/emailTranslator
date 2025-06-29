# LLM client connection
from openai import OpenAI
from emailTranslator.config import Config
from emailTranslator.logger import get_logger

logger = get_logger()


# Setup class incase later want to try switching betweem LLMs
class LLMClient:
    def __init__(self, api_key: str, model: str):
        logger.info("Starting LLMClient")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def parse_completion(self, messages, response_format):
        """
        For stuctured respones with pydantic use completions.parse
        """
        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model, messages=messages, response_format=response_format
            )

        except Exception as e:
            logger.error(f"LLM parse failed: {e}")
            raise

        results = completion.choices[0].message.parsed

        return results

    def create_completion(self, messages):
        """
        For non-structured chat responses if required
        """
        completion = self.client.chat.completions.create(
            model=self.model, messages=messages
        )

        return completion


def get_llm_client(llm="openai"):
    """
    Probably wont need a different llm but put this here in case.
    """
    if llm == "openai":
        client = LLMClient(api_key=Config.OPENAI_API_KEY, model=Config.OPENAI_MODEL)

    return client


if __name__ == "__main__":
    llm = get_llm_client()

    messages = [
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "What is the captical of Scotland?",
        },
    ]

    response = llm.create_completion(messages=messages)
    print(response.choices[0].message.content)
