from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name" : "john",
        "class" : "iot h2",
    }
}

class Student(BaseModel):
    name : str
    age : int
    year : int

@app.get("/")
def index():
    return {"hello":"world"}

@app.get("/get-students/{student_id}")
def get_student(student_id : int = Path(...,description ="the student data you wanted")):
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student(*,student_id : int ,name:Optional[str] = None,test:int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"data":"not found"}

@app.post("/create-student{student_id}")
def create_student(student_id : int , student : Student):
    if student_id in students:
        return {"error" : "student exist"}
    
    students[student_id] = student
    return students[student_id]