from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from chatbot import Chatbot

app = FastAPI()
bot = Chatbot()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5500"] for stricter control
    allow_methods=["*"],
    allow_headers=["*"]
)


class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(query: Query):
    response = bot.get_response(query.message)
    return {"response": response}  