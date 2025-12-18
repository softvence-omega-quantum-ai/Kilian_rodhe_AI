from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn as uv

from app.api.v1.endpoints import t_shirt_endpoint

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(t_shirt_endpoint.router)

@app.get("/")
def read_root():    
    return {"message": "Welcome to the Kilian Rodhe API.Image Generation Service"}
