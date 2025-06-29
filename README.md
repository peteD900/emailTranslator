# 📧 Email Translator/Summariser

A simple LLM agent used to translate email (or text) into English and them summarise the content
in bullet points. Also suggests if any actions were required. 

Built for fun to learn how to interact with LLMs using the OpenAI framework. A good resource
for learning is [Dave Ebbealaar AI cookbook](https://github.com/daveebbelaar/ai-cookbook).

## 👊 How it works

The project is currently split into two parts:

    1) Cloudflare email routing + worker 
     - Takes in a forwarded email 
     - Processes to extract sender, date, subject and body to plain text 
     - Forwards to an endpoint setup within this project 

    2) fastapi endpoint + LLM agent 
     - Recieves an email from the cloudflare worker 
     - Performs some security checks 
     - Translated the email if not in Englush and summarises 
     - Forwards a summay email to a default recipient 

### Cloudflare email routing and worker

This requires setting up separately. You need to register a domain 
with Cloudflare, then you can setup a email routing to forward on
emails sent to, for example, summarise@your_domain.xyx. I split
the worker out into a separate repo but I intend to put in back into
this project one day:

 - [Example email worker](https://github.com/peteD900/cf-worker-summariser)

### Endpont and LLM agent (this project)

I host the fastapi endpoint on a VPS. At the moment the config is not setup
to cleanly switch between modes (local/remote) for testing (to do). At the code 
is stored under emailTranslator (to do: rename). Structure:

```
./emailTranslator
├── config.py
├── emailer.py
├── __init__.py
├── llm.py
├── logger.py
├── main.py
├── models.py
├── safeguards.py
└── summariser.py
```

All the sensitive info pulled into config.py via a .env file. The fields required for .env:

# Code is all setup for openai structure
OPENAI_API_KEY = 

# Details of email client you use to send on the summarised email
EMAIL_USERNAME = 
EMAIL_PASSWORD = 
EMAIL_TO = 

# Make a token to share between email worker and this app
API_TOKEN = 

### Install

The project is not yet dockerised. I use uv pip and pyproject.toml to 
control dependancies for now. 

```python
uv pip install -r pyproject.toml

# or
pip install .
```

## To do

Extend README to show how to run app and send test email.