from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Institute 360")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.lower()

    if "schedule" in message or "timetable" in message:
        reply = "Please check the official student portal for your current class schedule."
    elif "contact" in message or "support" in message:
        reply = "Please check the institute website or student portal for student support contact details."
    elif "resource" in message or "campus" in message:
        reply = "Please check the student portal or institute website for campus resources."
    elif "enrollment" in message or "admission" in message:
        reply = "For enrollment or admission questions, please contact the institute office."
    else:
        reply = "I can help with class schedules, student support, campus resources, and enrollment. Which topic is your question about?"

    return {"reply": reply}