from fastapi import APIRouter

from app.services.updates import downloadIPA as iOS, downloadAPK as android
from app.config.config import CLIENT_UPDATING_TOKEN

router = APIRouter()

@router.get("/updateios/{authToken}")
async def updateiOS(authToken: str):
  if authToken != CLIENT_UPDATING_TOKEN:
    return {"error": "Cannot validate access token"}
  return await iOS()

@router.get("/updateandroid/{authToken}")
async def updateAndroid(authToken: str):
  if authToken != CLIENT_UPDATING_TOKEN:
    return {"error": "Cannot validate access token"}
  return await android()