# 📧 Email Translator & Summarizer

I setup this project to learn how to build LLM pipelines and setup "AI agents". The code in this repo will:

1. Translates incoming emails (or any text) into English  
2. Summarizes key points in concise bullet form  
3. Extracts any actions required

Built with Python, FastAPI, and OpenAI's framework. Inspiration from [Dave Ebbelaar’s AI Cookbook](https://github.com/daveebbelaar/ai-cookbook).

---

## 🧠 Architecture Overview

### 1. 📨 Cloudflare Email Routing & Worker

- Captures incoming email (e.g., to `summarise@your-domain.xyz`)
- Extracts sender, subject, date, and plain-text body
- Forwards this extracted email payload to your FastAPI endpoint

👉 Note: Worker lives in a separate repo — you can find an example [here](https://github.com/peteD900/cf-worker-summariser).

To do: move the worker into this project so it can be dockerised.

---

### 2. ⚙️ FastAPI Endpoint & LLM Agent

- Receives the processed email payload  
- Runs basic security/sanity checks  
- Translates to English (if needed) and summarizes via LLM  
- Sends a summarized email to a target recipient  

```bash
./emailTranslator/ # Main package (to be renamed someday 😅)
    ├── config.py # Loads credentials from .env
    ├── emailer.py # Email sending logic
    ├── llm.py # LLM prompting & interaction
    ├── summariser.py # Parsing/translating logic
    ├── safeguards.py # Input validation/security
    ├── logger.py # Structured logging
    ├── models.py # Pydantic request/response models
    └── main.py # FastAPI app entrypoint
```

---

## 🔧 Configuration (`.env` variables)

```bash
OPENAI_API_KEY=… # Your OpenAI API key
EMAIL_USERNAME=… # SMTP username
EMAIL_PASSWORD=… # SMTP password or app-specific password
EMAIL_TO=… # Where summary emails should be sent
API_TOKEN=… # Shared secret between CF Worker & this FastAPI app
```


---

## 🚀 Getting Started

### 1. Install dependencies

```bash
# Using pip (non‑docker, pure Python)
pip install .
# or
uv pip install -r pyproject.toml
```

### 2. Configure .env

Populate .env with values from above section.

### 3. Run the FastAPI service

```bash
uvicorn emailTranslator.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test it locally

Use tools like curl or Postman:

```bash
curl -X POST "http://localhost:8000/email" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "sender": "jorge@example.com",
        "subject": "Nueva oferta :)",
        "date": "2025-06-29T12:00:00",
        "body": "¡Hola! Quería saber si podemos reunirnos mañana a las 2."
      }'
```

You should receive a summarized & translated email at EMAIL_TO.

🧩 TODOs

 - Dockerize

 - Ease config switching (local/dev/prod)

 - Add tests

 - Merge Cloudflare worker code into main repo