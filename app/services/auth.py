import hashlib
import uuid
from datetime import datetime, timedelta

from app.models.models import Session
from app.services.storage import load, dump, delete
from app.services.realtime import getRtime

async def login(userID: str, password: str):
  loginOk = False
  user = await load("users", userID)
  if user == None: return {"error": "The user with the specified ID does not exist"}
  passwdHash = hashlib.sha256(password.encode("utf-8")).hexdigest()
  if user.password == "":
    user.password = passwdHash
    modification = await dump("users", user)
    if modification:
      loginOk = True
      await getRtime().notify("users")
    else:
      return {"error": "An error occurred while trying to modify the user"}
  else:
    loginOk = user.password == passwdHash
  
  if loginOk:
    date = datetime.now()
    date = date + timedelta(weeks=4)
    newSession = Session(
      id=str(uuid.uuid4()),
      user=userID,
      expiryDate=date.strftime("%Y-%m-%d %H:%M:%S.%f")
    )
    addition = await dump("sessions", newSession)
    if addition:
      await getRtime().notify("sessions")
      authToken = await _genAuthToken(newSession.id)
      return {"session": newSession, "authToken": authToken}
    else:
      return {"error": "An error occurred while trying to add the session"}
  return {"error": "The user with the specified ID does not exist, or the password is incorrect"}

async def logout(sessionID: str):
  session = await load("sessions", sessionID)
  if session == None: return {"error": "The session with the specified ID does not exist"}
  deletion = await delete("sessions", sessionID)

  if deletion:
    await getRtime().notify("sessions")
    return {"ok": ""}
  return {"error": "An error occurred while trying to delete the session"}

async def changePasswd(userID: str, sessionID: str, oldPasswd: str, newPasswd: str):
  user = await load("users", userID)
  if user == None: return {"error": "The user with the specified ID does not exist"}
  passwdHash = hashlib.sha256(oldPasswd.encode("utf-8")).hexdigest()
  if user.password == passwdHash:
    user.password = hashlib.sha256(newPasswd.encode("utf-8")).hexdigest()
    modification = await dump("users", user)
    if modification:
      token = await _genAuthToken(sessionID)
      return {"authToken": token}
    else:
      return {"error": "An error occurred while trying to modify the user"}
  return {"error": "The current password entered is incorrect"}

async def _genAuthToken(sessionID: str) -> str:
  session = await load("sessions", sessionID)
  if session == None: return {"error": "The session with the specified ID does not exist"}
  user = await load("users", session.user)
  if user == None: return {"error": "The user with the specified ID does not exist"}

  token = session.id + session.expiryDate + user.id + user.password
  token = hashlib.sha256(token.encode("utf-8")).hexdigest()
  return token

async def validateOperation(sessionID: str, authToken: str) -> bool:
  return True
  """ ///* COMMENTED TO AVOID VALID USER AND SESSION CHECKS *///
  session = await load("sessions", sessionID)
  if session == None: return False
  user = await load("users", session.user)
  if user == None: return False

  token = session.id + session.expiryDate + user.id + user.password
  token = hashlib.sha256(token.encode("utf-8")).hexdigest()
  if token == authToken: return True
  return False
  """