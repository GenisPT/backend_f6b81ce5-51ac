from fastapi import APIRouter
from app.services.auth import login as loginFunc, logout as logoutFunc, changePasswd as changePasswdFunc, validateOperation

router = APIRouter()

@router.get("/login/{userID}/{password}")
async def login(userID: str, password: str):
  return await loginFunc(userID=userID, password=password)

@router.get("/logout/{sessionID}/{authToken}")
async def logout(sessionID: str, authToken: str):
  if not await validateOperation(sessionID, authToken):
    return {"error": "Cannot validate access token"}
  return await logoutFunc(sessionID)

@router.put("/changepasswd/{userID}/{sessionID}/{oldPasswd}/{newPasswd}/{authToken}")
async def changePasswd(userID: str, sessionID: str, oldPasswd: str, newPasswd: str, authToken: str):
  if not await validateOperation(sessionID, authToken):
    return {"error": "Cannot validate access token"}
  return await changePasswdFunc(userID, sessionID, oldPasswd, newPasswd)