"""
  GenAI Agent-Based SQL Assistant
  Multi-agent NL-to-SQL system with RAG pipeline and guardrails.
  """
  import os
  from dotenv import load_dotenv
  from fastapi import FastAPI, HTTPException
  from pydantic import BaseModel
  from langchain_openai import ChatOpenAI, OpenAIEmbeddings
  from langchain.chains import RetrievalQA
  from langchain_community.vectorstores import Pinecone as PineconeVectorStore
  from langchain.prompts import PromptTemplate
  import pinecone

  load_dotenv()

  app = FastAPI(title="GenAI SQL Assistant", version="1.0.0")

  # ── LLM & Embeddings ──────────────────────────────────────────────────────
  llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
  embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

  # ── Schema Context Prompt ─────────────────────────────────────────────────
  SQL_PROMPT = PromptTemplate(
      input_variables=["schema_context", "question"],
      template="""You are an expert SQL generator. Use the schema context below to write
  a precise SQL query. Return ONLY the SQL query, nothing else.

  Schema Context:
  {schema_context}

  Question: {question}

  SQL Query:"""
  )

  # ── Intent Classification ─────────────────────────────────────────────────
  INTENT_PROMPT = PromptTemplate(
      input_variables=["question"],
      template="""Classify this database question into one of: SELECT, AGGREGATE, JOIN, FILTER, UNKNOWN.
  Question: {question}
  Intent:"""
  )


  class QueryRequest(BaseModel):
      question: str
      schema: dict


  class QueryResponse(BaseModel):
      sql: str
      intent: str
      confidence: float


  def classify_intent(question: str) -> str:
      chain = INTENT_PROMPT | llm
      result = chain.invoke({"question": question})
      return result.content.strip()


  def validate_sql(sql: str, schema: dict) -> tuple[bool, float]:
      """Basic SQL validation and confidence scoring."""
      tables = list(schema.get("tables", {}).keys())
      mentioned_tables = [t for t in tables if t.lower() in sql.lower()]
      confidence = len(mentioned_tables) / max(len(tables), 1)
      is_valid = sql.strip().upper().startswith(("SELECT", "WITH"))
      return is_valid, round(confidence, 2)


  def build_schema_context(schema: dict) -> str:
      lines = []
      for table, cols in schema.get("tables", {}).items():
          col_defs = ", ".join(f"{c['name']} {c['type']}" for c in cols)
          lines.append(f"Table {table}: ({col_defs})")
      return "\n".join(lines)


  @app.post("/query", response_model=QueryResponse)
  async def generate_sql(request: QueryRequest):
      schema_context = build_schema_context(request.schema)
      intent = classify_intent(request.question)

      chain = SQL_PROMPT | llm
      result = chain.invoke({"schema_context": schema_context, "question": request.question})
      sql = result.content.strip()

      is_valid, confidence = validate_sql(sql, request.schema)
      if not is_valid:
          raise HTTPException(status_code=422, detail="Generated SQL failed validation")

      return QueryResponse(sql=sql, intent=intent, confidence=confidence)


  @app.get("/health")
  def health():
      return {"status": "online", "model": "gpt-4o-mini"}


  if __name__ == "__main__":
      import uvicorn
      uvicorn.run(app, host="0.0.0.0", port=8000)
  