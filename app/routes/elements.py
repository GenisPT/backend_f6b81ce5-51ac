"""
Generic CRUD endpoints for managing data collections.

Allows:
- Retrieving elements
- Creating elements
- Updating elements
- Deleting elements
"""

from fastapi import APIRouter
from app.models.models import ValidateElementType
from app.services.storage import resolveCollection, dump
from app.services.realtime import notifyChanges

router = APIRouter()

"""
Returns a specific element from a collection
or the entire collection.
"""
@router.get("/fetch/{collectionID}/{id}")
def fetchElement(collectionID: str, id: str):
  collection = resolveCollection(collectionID)
  if isinstance(collection, list):
    if id != "all":
      for elem in collection:
        if elem.id == id:
          return elem
      return {"error": "The item with the specified ID was not found"}
    else:
      return collection
  else:
    return {"error": "(Server Error): The specified item collection does not exist"}

# Creates a new element inside a collection.
@router.post("/create/{collectionID}")
async def createElement(collectionID: str, element: ValidateElementType):
  collection = resolveCollection(collectionID)
  if isinstance(collection, list):
    for elem in collection:
      if elem.id == element.id:
        return {"error": "The item you are trying to create already exists"}
    collection.append(element)
    dump(collectionID)
    await notifyChanges(collectionID)
    return {"ok": ""}
  else:
    return {"error": "(Server Error): The specified item collection does not exist"}

# Updates an existing element in a collection.
@router.put("/update/{collectionID}")
async def updateElement(collectionID: str, element: ValidateElementType):
  collection = resolveCollection(collectionID)
  if isinstance(collection, list):
    for elem, idx in zip(collection, range(len(collection))):
      if elem.id == element.id:
        collection[idx] = element
        dump(collectionID)
        await notifyChanges(collectionID)
        return {"ok": ""}
    return {"error": "The item with the specified ID was not found"}
  else:
    return {"error": "(Server Error): The specified item collection does not exist"}

# Removes an element from a collection.
@router.delete("/remove/{collectionID}/{id}")
async def removeElement(collectionID: str, id: str):
  collection = resolveCollection(collectionID)
  if isinstance(collection, list):
    for elem in collection:
      if elem.id == id:
        collection.remove(elem)
        dump(collectionID)
        await notifyChanges(collectionID)
        return {"ok": ""}
    return {"error": "The item with the specified ID was not found"}
  else:
    return {"error": "(Server Error): The specified item collection does not exist"}