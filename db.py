import os
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# MongoDB connection URI
MONGO_URI = os.getenv("DB_URL")

# Initialize MongoDB client
client = MongoClient(MONGO_URI)

#database and collection
db = client.student
collection = db.registrations