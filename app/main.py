from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from app.rag import answer_question

app = FastAPI(title="ResolveAgent")

class AskRequest(BaseModel):
    question:str

class Source(BaseModel):
    title: str
    url: str
    score: float

class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    input_tokens: int
    output_tokens: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        return answer_question(req.question)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Answering failed: {e}")
