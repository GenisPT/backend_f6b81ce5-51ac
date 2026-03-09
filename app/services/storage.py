"""
Data persistence service.

Handles loading and saving collections into JSON files
which act as a simple database for the application.
"""

import json
from pathlib import Path
from typing import get_args
from app.models.models import *
from app.config import PERSISTENT_DATA_PATH

"""
Attempts to validate a dictionary against all possible models
and returns the matching model instance.
"""
def resolveElement(data: dict) -> BaseModel:
  for model in get_args(ValidateElementType):
    try:
      return model.model_validate(data)
    except:
      pass

"""
Loads a collection from the corresponding JSON file
and converts its elements into Pydantic model instances.
"""
def load(collectionID: str):
  try:
    with open(PERSISTENT_DATA_PATH + collectionID + ".json", "r", encoding="utf-8") as file:
      data = json.load(file)
      return [resolveElement(element) for element in data]
  except:
    Path(PERSISTENT_DATA_PATH).mkdir(exist_ok=True)
    with open(PERSISTENT_DATA_PATH + collectionID + ".json", "w", encoding="utf-8") as file:
      json.dump([], file)
    return []

"""
Saves a collection of Pydantic models into the corresponding
JSON file by serializing them into dictionaries.
"""
def dump(collectionID: str):
  collection = resolveCollection(collectionID)
  try:
    with open(PERSISTENT_DATA_PATH + collectionID + ".json", "w", encoding="utf-8") as file:
      data = [resolveElement(element).model_dump() for element in collection]
      json.dump(data, file, indent=2, ensure_ascii=False)
  except:
    pass

# Initialize collections by loading data from JSON files
tables: list[Table] = load("tables")
items: list[Item] = load("items")
clientItems: list[ClientItem] = load("clientitems")
kitchens: list[Kitchen] = load("kitchens")
users: list[User] = load("users")
sessions: list[Session] = load("sessions")
notifications: list[Notification] = load("notifications")
tickets: list[Ticket] = load("tickets")
ticketItems: list[TicketItem] = load("ticketitems")
licenses: list[License] = load("licenses")

"""
Returns the in-memory list corresponding to the
specified collection identifier.
"""
def resolveCollection(id: str):
  return {
    "tables": tables,
    "items": items,
    "clientitems": clientItems,
    "kitchens": kitchens,
    "users": users,
    "sessions": sessions,
    "notifications": notifications,
    "tickets": tickets,
    "ticketitems": ticketItems,
    "licenses": licenses
  }.get(id)