import json
import orjson
import redis.asyncio as rclient
from filelock import FileLock

from app.models.models import *
from app.config.config import PERSISTENT_DATA_PATH

_redis: rclient.Redis | None = None

COLLECTIONS = [
  "tables", "items", "clientitems", "kitchens",
  "users", "sessions", "notifications", "tickets",
  "ticketitems", "licenses", "printing"
]

def initRedis(url: str, decodeResponses: bool):
  global _redis
  _redis = rclient.from_url(
    url,
    decode_responses=decodeResponses
  )

def getRedis() -> rclient.Redis:
  global _redis
  return _redis

def resolveElement(data: dict) -> BaseModel:
  dataType = data.get("type")
  classType = {
    "table": Table,
    "item": Item,
    "clientitem": ClientItem,
    "kitchen": Kitchen,
    "user": User,
    "session": Session,
    "notification": Notification,
    "ticket": Ticket,
    "ticketitem": TicketItem,
    "license": License,
    "print": Print,
    "group": Group
  }.get(dataType)
  return classType(**data)

async def load(collectionID: str, elementID: str | None = None) -> BaseModel | list[BaseModel] | None:
  try:
    if elementID == None:
      keySet = f"{collectionID}:ids"
      allKeys = await _redis.smembers(keySet)

      collection: list[BaseModel] = []
      for id in allKeys:
        key = f"{collectionID}:{id}"
        data = await _redis.get(key)
        if not data:
          continue

        data = orjson.loads(data)
        elem = resolveElement(data)
        collection.append(elem)
      return collection
    else:
      key = f"{collectionID}:{elementID}"
      data = await _redis.get(key)
      data = orjson.loads(data)
      elem = resolveElement(data)
      return elem
  except:
    return None

async def dump(collectionID: str, toDump: BaseModel) -> bool:
  try:
    keySet = f"{collectionID}:ids"
    key = f"{collectionID}:{toDump.id}"
    data = orjson.dumps(toDump.model_dump()).decode()

    await _redis.set(key, data)
    await _redis.sadd(keySet, toDump.id)
    return True
  except Exception as e:
    print(e)
    return False

async def delete(collectionID: str, elementID: str) -> bool:
  try:
    keySet = f"{collectionID}:ids"
    key = f"{collectionID}:{elementID}"

    await _redis.delete(key)
    await _redis.srem(keySet, elementID)
    return True
  except:
    return False

async def pull() -> int:
  errors = 0
  for collectionID in COLLECTIONS:
    collection = await load(collectionID)
    path = f"{PERSISTENT_DATA_PATH}{collectionID}.json"
    lock = FileLock(f"{path}.lock")

    with lock:
      try:
        with open(path, "w", encoding="utf-8") as file:
          data = [elem.model_dump() for elem in collection]
          json.dump(data, file, indent=2, ensure_ascii=False)
      except:
        errors += 1
        continue
  return errors

async def push() -> int:
  errors = 0
  for collectionID in COLLECTIONS:
    try:
      with open(PERSISTENT_DATA_PATH + collectionID + ".json", "r", encoding="utf-8") as file:
        data = json.load(file)
        elements = [resolveElement(elem) for elem in data]

        keySet = f"{collectionID}:ids"
        allKeys = await _redis.smembers(keySet)
        keys = [f"{collectionID}:{id}" for id in allKeys]
        if len(keys) > 0:
          await _redis.delete(*keys)
        await _redis.delete(keySet)

        for elem in elements:
          isOK = await dump(collectionID, elem)
          if not isOK: errors += 1
    except:
      errors += 1
      continue
  return errors