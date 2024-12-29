"""FastAPI application for text analysis and anonymization."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import analysis, anonymization, health

# Get configuration from environment variables
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_ROOT_PATH = os.getenv("API_ROOT_PATH", "/api/v1")

app = FastAPI(
    title="Presidio-NL API",
    description="API voor Nederlandse tekst analyse en anonimisatie",
    version="0.1.0",
    root_path=API_ROOT_PATH
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configureer dit in productie
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(analysis.router)
app.include_router(anonymization.router) 