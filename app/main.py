"""
FastAPI application entry point.

Responsible for:
- Creating the FastAPI instance
- Configuring CORS middleware
- Registering routers
- Defining basic endpoints such as /ping
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.routes import elements, auth, licenses
from app.services.realtime import router as rtime_router

app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
  CORSMiddleware,
  allow_origins=ALLOWED_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(elements.router)
app.include_router(auth.router)
app.include_router(licenses.router)
app.include_router(rtime_router)

@app.get("/ping")
def ping():
  return "Pong!"