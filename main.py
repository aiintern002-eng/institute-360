from typing import List

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(
    title="Institute 360 API",
    description="Student and chatbot REST API",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


class StudentCreate(BaseModel):
    name: str
    email: str
    course: str


class Student(StudentCreate):
    student_id: int


students: List[Student] = []
next_student_id = 1


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/api/health")
def health():
    return {
        "application": "Institute 360",
        "status": "Running"
    }


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
        reply = "I can help with class schedules, student support, campus resources, and enrollment."

    return {"reply": reply}


@app.get("/students", response_model=List[Student])
def get_students():
    return students


@app.post(
    "/students",
    response_model=Student,
    status_code=status.HTTP_201_CREATED
)
def add_student(student: StudentCreate):
    global next_student_id

    new_student = Student(
        student_id=next_student_id,
        name=student.name,
        email=student.email,
        course=student.course
    )

    students.append(new_student)
    next_student_id += 1

    return new_student


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for student in students:
        if student.student_id == student_id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: StudentCreate):
    for index, student in enumerate(students):
        if student.student_id == student_id:
            students[index] = Student(
                student_id=student_id,
                name=updated_student.name,
                email=updated_student.email,
                course=updated_student.course
            )
            return students[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student.student_id == student_id:
            students.pop(index)
            return {"message": "Student deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )
