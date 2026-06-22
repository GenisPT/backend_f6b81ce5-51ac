import uuid
import random
from fastapi import APIRouter


from app.models.models import License
from app.services.storage import load, dump
from app.services.realtime import getRtime
from app.services.auth import validateOperation

router = APIRouter()

async def genKey() -> str:
  licenses = await load("licenses")
  keyValid = False
  letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
  numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
  key = []

  while(not keyValid):
    keyValid = True
    key.clear()
    nLetters = random.randint(1, 10)
    nNumbers = 10 - nLetters

    for _ in range(0, nLetters):
      key.append(random.choice(letters))
    for _ in range(0, nNumbers):
      key.append(random.choice(numbers))
    random.shuffle(key)

    for license in licenses:
      if license.key == key:
        keyValid = False
        break
  return "".join(key)

@router.post("/genlicense/{tag}/{maxUses}/{expiryDate}/{sessionID}/{authToken}")
async def genLicense(tag: str, maxUses: int, expiryDate: str, sessionID: str, authToken: str):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}
  newLicense = License(
    id=str(uuid.uuid4()),
    tag=tag,
    key=await genKey(),
    maxUses=maxUses,
    activations=[],
    expiryDate=expiryDate
  )
  addition = await dump("licenses", newLicense)
  if addition:
    await getRtime().notify("licenses")
    return newLicense
  return {"error": "Error while creating license"}