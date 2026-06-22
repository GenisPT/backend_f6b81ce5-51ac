from fastapi import APIRouter, Body
from typing import List, Annotated
from pydantic import Field

from app.models.models import ValidateElementType
from app.services.storage import load, dump, delete, pull as pullFromRedis, push as pushToRedis, COLLECTIONS, resolveElement
from app.services.realtime import getRtime
from app.services.auth import validateOperation

router = APIRouter()

@router.get("/fetch/{collectionID}/{id}/{sessionID}/{authToken}")
async def fetchElement(collectionID: str, id: str, sessionID: str, authToken: str):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}
  if id != "all":
    elem = await load(collectionID, id)
    if elem is None: return {"error": "The element with the specified ID does not exist"}
    return elem
  else:
    elems = await load(collectionID)
    return elems

@router.post("/create/{collectionID}/{sessionID}/{authToken}")
async def createElement(collectionID: str, sessionID: str, authToken: str, element: ValidateElementType):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}
  exists = await load(collectionID, element.id)

  if exists is None:
    addition = await dump(collectionID, element)
    if addition:
      await getRtime().notify(collectionID)
      return {"ok": ""}
    return {"error": "Error while adding current element"}
  return {"error": "This element ID already exists"}

@router.post("/mcreate/{sessionID}/{authToken}")
async def createElements(sessionID: str, authToken: str, element: ValidateElementType):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}

  results: list[bool] = []
  for elem in element.elements:
    model = resolveElement(elem)
    exists = await load(element.collectionID, model.id)

    if exists is None:
      addition = await dump(element.collectionID, model)
      if addition:
        results.append(True)
      else:
        results.append(False)
    else:
      results.append(False)
  
  if True in results and False in results:
    await getRtime().notify(element.collectionID)
    return {"error": "Some items were processed successfully and some were not, because some of the item IDs already exist"}
  elif True in results:
    await getRtime().notify(element.collectionID)
    return {"ok": ""}
  else:
    return {"error": "None of the items were processed successfully because their IDs already exist"}

@router.put("/update/{collectionID}/{sessionID}/{authToken}")
async def updateElement(collectionID: str, sessionID: str, authToken: str, element: ValidateElementType):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}
  exists = await load(collectionID, element.id)

  if exists is not None:
    modification = await dump(collectionID, element)
    if modification:
      await getRtime().notify(collectionID)
      return {"ok": ""}
    return {"error": "Error while updating current element"}
  return {"error": "This element ID doesn't exist"}

@router.put("/mupdate/{sessionID}/{authToken}")
async def updateElements(sessionID: str, authToken: str, element: ValidateElementType):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}

  results: list[bool] = []
  for elem in element.elements:
    model = resolveElement(elem)
    exists = await load(element.collectionID, model.id)

    if exists is not None:
      modification = await dump(element.collectionID, model)
      if modification:
        results.append(True)
      else:
        results.append(False)
    else:
      results.append(False)
  
  if True in results and False in results:
    await getRtime().notify(element.collectionID)
    return {"error": "Some items were processed successfully and some were not, because some of the item IDs already exist"}
  elif True in results:
    await getRtime().notify(element.collectionID)
    return {"ok": ""}
  else:
    return {"error": "None of the items were processed successfully because their IDs already exist"}

@router.delete("/remove/{collectionID}/{id}/{sessionID}/{authToken}")
async def removeElement(collectionID: str, id: str, sessionID: str, authToken: str):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}

  exists = await load(collectionID, id)

  if exists is not None:
    deletion = await delete(collectionID, id)
    if deletion:
      await getRtime().notify(collectionID)
      return {"ok": ""}
    return {"error": "Error while deleting current element"}

@router.delete("/mremove/{sessionID}/{authToken}")
async def removeElements(sessionID: str, authToken: str, element: ValidateElementType):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}

  results: list[bool] = []
  for elem in element.elements:
    model = resolveElement(elem)
    exists = await load(element.collectionID, model.id)

    if exists is not None:
      deletion = await delete(element.collectionID, model.id)
      if deletion:
        results.append(True)
      else:
        results.append(False)
    else:
      results.append(False)
  
  if True in results and False in results:
    await getRtime().notify(element.collectionID)
    return {"error": "Some items were processed successfully and some were not, because some of the item IDs already exist"}
  elif True in results:
    await getRtime().notify(element.collectionID)
    return {"ok": ""}
  else:
    return {"error": "None of the items were processed successfully because their IDs already exist"}

@router.get("/pull/{sessionID}/{authToken}")
async def pull(sessionID: str, authToken: str):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}

  errors = await pullFromRedis()
  if errors == 0:
    return {"ok": ""}
  return {"error": f"There were a total of {errors} errors in the data retrieval process"}

@router.post("/push/{sessionID}/{authToken}")
async def push(sessionID: str, authToken: str):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}

  errors = await pushToRedis()
  if errors == 0:
    for collectionID in COLLECTIONS:
      await getRtime().notify(collectionID)
    return {"ok": ""}
  return {"error": f"There were a total of {errors} errors in the data submission process"}