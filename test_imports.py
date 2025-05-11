from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

print("All imports successful!")

# Test FastAPI
app = FastAPI()
print("FastAPI app created successfully!")

# Test CORS
app.add_middleware(CORSMiddleware)
print("CORS middleware added successfully!")

# Test environment loading
load_dotenv()
print("Environment loaded successfully!")

# Test MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017/")
print("MongoDB client created successfully!") 