"""
Authentication service.

Responsible for:
- User login and session creation
- User logout and session deletion
- Password modification
"""

import hashlib
import uuid
from datetime import datetime, timedelta

from app.models.models import Session
from app.services.storage import users, sessions, dump
from app.services.realtime import notifyChanges

# Authenticates a user and creates a new session with expiration.
async def login(userID: str, password: str):
  loginOk = False
  for user in users:
    if user.id == userID:
      # Hash the password using SHA256
      passwdHash = hashlib.sha256(password.encode("utf-8")).hexdigest()
      # If the user has no password set, define it on first login
      if user.password == "":
        user.password = passwdHash
        loginOk = True
        dump("users")
        await notifyChanges("users")
      else:
        loginOk = user.password == passwdHash
      break
  
  if loginOk:
    date = datetime.now()
    date = date + timedelta(weeks=4)
    newSession = Session(
      id=str(uuid.uuid4()),
      user=userID,
      expiryDate=date.strftime("%Y-%m-%d %H:%M:%S.%f")
    )
    sessions.append(newSession)
    dump("sessions")
    await notifyChanges("sessions")
    return newSession
  return {"error": "User with the specified ID not found"}

# Removes an active session.
async def logout(sessionID: str):
  for session in sessions:
    if session.id == sessionID:
      sessions.remove(session)
      dump("sessions")
      await notifyChanges("sessions")
  return {"ok": ""}

# Changes a user's password if the current password is correct.
async def changePasswd(userID: str, oldPasswd: str, newPasswd: str):
  for user in users:
    if user.id == userID:
      passwdHash = hashlib.sha256(oldPasswd.encode("utf-8")).hexdigest()
      if user.password == passwdHash:
        user.password = hashlib.sha256(newPasswd.encode("utf-8")).hexdigest()
        dump("users")
        return {"ok": ""}
      return {"error": "The current password you entered is incorrect"}
  return {"error": "User with the specified ID not found"}