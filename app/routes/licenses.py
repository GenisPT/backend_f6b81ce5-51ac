"""
Endpoints related to license generation and management.
"""

from fastapi import APIRouter
import uuid
import random

from app.models.models import License
from app.services.storage import licenses, dump
from app.services.realtime import notifyChanges

router = APIRouter()

"""
Generates a unique 10-character license key composed
of random letters (uppercased) and numbers.
"""
def genKey() -> str:
  keyValid = False
  letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
  numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
  key = []

  # Ensure the generated key does not already exist
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

"""
Generates a new license with a usage limit and
expiration date.
"""
@router.post("/genlicense/{tag}/{maxUses}/{expiryDate}")
async def genLicense(tag: str, maxUses: int, expiryDate: str):
  newLicense = License(
    id=str(uuid.uuid4()),
    tag=tag,
    key=genKey(),
    maxUses=maxUses,
    activations=[],
    expiryDate=expiryDate
  )
  licenses.append(newLicense)
  dump("licenses")
  await notifyChanges("licenses")
  return newLicense