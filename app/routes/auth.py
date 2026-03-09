"""
Endpoints related to authentication and
session management.
"""

from fastapi import APIRouter
from app.services.auth import login as loginFunc, logout as logoutFunc, changePasswd as changePasswdFunc

router = APIRouter()

# Login endpoint that creates a session if the credentials are valid.
@router.get("/login/{userID}/{password}")
async def login(userID: str, password: str):
  return loginFunc

# Ends an active session.
@router.get("/logout/{sessionID}")
async def logout(sessionID: str):
  return logoutFunc

# Changes a user's password.
@router.put("/changepasswd/{userID}/{oldPasswd}/{newPasswd}")
async def changePasswd(userID: str, oldPasswd: str, newPasswd: str):
  return changePasswdFunc