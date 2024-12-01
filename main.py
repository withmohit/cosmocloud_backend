from fastapi import FastAPI, HTTPException
from bson import ObjectId
from pydantic import BaseModel
from db import collection, serialize_document

app = FastAPI()

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address


# To fetch all student registrations
@app.get('/students')
def get_students():
    students = collection.find()  
    return [serialize_document(student) for student in students]

# To insert a new student
@app.post("/students", status_code=201)
def create_student(student: Student):
    student_dict = student.model_dump()
    result = collection.insert_one(student_dict)
    return {"id": str(result.inserted_id)}
