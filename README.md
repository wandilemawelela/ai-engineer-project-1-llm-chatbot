# Project 1: LLM Setup and Basic Chatbot

## Project Overview
This project is the foundation of an AI-powered chatbot built using a Large Language Model (LLM) API.  
By Day 7, it will evolve into a command-line chatbot with:

- Token usage tracking
- Cost awareness
- Structured JSON outputs
- Optimized prompt handling
- Environment-based configuration

The goal is to deeply understand how LLMs work in real-world applications, including API interaction, context management, and cost control.

---

## LLM Provider
**Google Gemini**

> *(The provider may later change to Anthropic or Google Gemini for comparison and experimentation.)*

---

## Tech Stack
- Python 3.10+
- OpenAI / Gemini SDK (provider-dependent)
- `python-dotenv` for environment variables
- Command-line interface (CLI)

---

## ⚙️ Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/wandilemawelela/ai-engineer-project-1-llm-chatbot.git
cd ai-engineer-project-1-llm-chatbot
```

---

### Create and Activate a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
```

---

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Set Up Environment Variables

#### Copy `.env.example` to `.env`
```bash
cp .env.example .env
```

#### Update `.env` with Your API Key
Open `.env` and add your API key:
```env
OPENAI_API_KEY=your_api_key_here
```

or (if using Gemini later):
```env
GOOGLE_API_KEY=your_api_key_here
```

---

### Important Security Reminder
- **DO NOT commit `.env` to GitHub**
- Ensure `.env` is listed in `.gitignore`
- API keys should **never** be hardcoded in source files

Example `.gitignore` entry:
```gitignore
.env
venv/
```

---

## Running the Chatbot
```bash
python main.py
```

---

## Project Goals & Deliverables

By the end of this project, the chatbot will include:
- LLM API integration
- Token usage tracking
- Cost estimation per request
- Structured JSON responses
- Optimized system and user prompts
- Clean CLI interface

---

## Learning Outcomes
This project focuses on:
- Understanding how LLM APIs work
- Managing context windows and tokens
- Secure API key handling
- Designing scalable AI-powered applications

---

## Future Enhancements
- Provider switching (OpenAI ↔ Gemini ↔ Anthropic)
- Conversation memory
- Streaming responses
- Logging & analytics
- Web interface

