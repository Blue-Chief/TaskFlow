from fastapi import FastAPI

app = FastAPI()

app.get("/")
async def home():
    return {"message" : "Welcome to TaskFlow"}

app.get("/health/")
async def health_status():
    return {"status" : "Healthy"}