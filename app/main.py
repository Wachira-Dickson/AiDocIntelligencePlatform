from fastapi import FastAPI

# Register the models with SQLAlchemy
from app.db import models

from app.routers import auth, documents


app = FastAPI(
    title="AI Document Intelligence Platform",
    description="Backend API for document upload and intelligent document processing.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(documents.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Document Intelligence Platform API"}