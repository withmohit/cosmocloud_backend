from fastapi import FastAPI, HTTPException
from bson import ObjectId
from pydantic import BaseModel
from db import collection

app = FastAPI()

# Model for student info
class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

#  Model for updates/patch
class StudentUpdate(BaseModel):
    name: str|None = None
    age: int|None = None
    address: Address|None = None


# To fetch all student registrations with filters
@app.get('/students',status_code=200)
def get_students(country:str|None=None, age:int|None=None):
    filter_query=dict()
    if country: filter_query['address.country']=country
    if age: filter_query['age']={'$gte':age}
    students = collection.find(filter_query, {'name':1,'age':1,'_id':0})  
    return {"data":[student for student in students]}

# To insert a new student
@app.post("/students", status_code=201)
def create_student(student: Student):
    student_dict = student.model_dump()
    result = collection.insert_one(student_dict)
    return {"id": str(result.inserted_id)}

# To query a particular student with id
@app.get('/students/{id}',status_code=200)
def find_student(id:str):
    result=collection.find_one({'_id':ObjectId(id)}, {'_id':0,'name':1,'age':1,'address':1})
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return result

# To update info of student
@app.patch('/students/{id}',status_code=204)
def update_student(id:str,updated_info:StudentUpdate):
    id=ObjectId(id)
    updated_info=updated_info.model_dump(exclude_unset=True)
    if not updated_info:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    result=collection.update_one({'_id':id},{'$set':updated_info})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

# To delete a particular student info
@app.delete('/students/{id}',status_code=200)
def delete_student(id:str):
    id=ObjectId(id)
    result=collection.delete_one({'_id':id})
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")