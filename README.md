# GenAI Agent-Based SQL Assistant

  An LLM-powered Natural Language to SQL system built by Ankit Kumar — AI/GenAI Engineer with 3+ years of experience designing and shipping production AI systems.

  ## Overview
  Multi-agent orchestration pipeline that converts natural language queries into accurate SQL using RAG, schema-aware prompting, and LangChain.

  ## Features
  - Natural language → SQL translation via LangChain + OpenAI
  - Schema-aware prompting with context injection
  - RAG pipeline with Pinecone to reduce hallucinations by 30%
  - Multi-agent orchestration (intent → planning → SQL gen → validation)
  - 20–25% latency reduction via retrieval optimization
  - FastAPI backend handling 5K–10K requests/day
  - Guardrails: validation layers, confidence scoring, execution checks
  - n8n workflow automation for API integrations

  ## Architecture
  ```
  User Query → Intent Agent → Schema Context (RAG) → SQL Generator → Validator → DB Executor
  ```

  ## Tech Stack
  Python · LangChain · OpenAI · Pinecone · FastAPI · n8n · Docker

  ## Setup
  ```bash
  pip install -r requirements.txt
  cp .env.example .env   # add your API keys
  uvicorn main:app --reload
  ```

  ## Metrics
  | Metric | Before | After |
  |--------|--------|-------|
  | Query Accuracy | 70% | 85% |
  | Hallucinations | baseline | -30% |
  | Latency | baseline | -20–25% |
  | API Cost | baseline | -15–20% |

  ## Contact
  **Ankit Kumar** · ankitthakur104@gmail.com · [GitHub](https://github.com/ankitthakur104)
  