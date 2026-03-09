"""
Data models used by the API.

Models are defined using Pydantic to validate and serialize
data received and returned by the endpoints.
"""

from pydantic import BaseModel
from typing import Union

# ===== Restaurant ===== #
class Table(BaseModel):
  id: str
  name: str
  status: str
  persons: int
  waitersID: str
  waitersName: str

class Item(BaseModel):
  id: str
  tableID: str
  name: str
  description: str
  isKitchen: bool
  status: str
  waiterID: str
  waiterName: str
  quantity: int
  paid: int
  category: str
  orderDatetime: str
  servedDatetime: str
  price: float
  
  apparentTemp: float
  precipitation: float
  weatherStatus: str
  cloudCover: float
  windSpeed: float
  windDirection: float

class ClientItem(BaseModel):
  id: str
  name: str
  isKitchen: bool
  category: str
  price: float

class Kitchen(BaseModel):
  id: str
  status: str

# ===== Orders ===== #
class Ticket(BaseModel):
  id: str
  tableName: str
  waiterName: str
  openedDatetime: str
  closedDatetime: str
  persons: int
  paid: float
  paymentType: str
  registered: bool

class TicketItem(BaseModel):
  id: str
  ticketID: str
  name: str
  isKitchen: bool
  waiterID: str
  quantity: int
  orderDatetime: str
  servedDatetime: str
  category: str
  price: float
  discount: float

  apparentTemp: float
  precipitation: float
  weatherStatus: str
  cloudCover: float
  windSpeed: float
  windDirection: float

# ===== Authentication ===== #
class User(BaseModel):
  id: str
  password: str
  name: str
  surname: str
  roles: list[str]

class Session(BaseModel):
  id: str
  user: str
  expiryDate: str

# ===== System ===== #

class Notification(BaseModel):
  id: str
  user: str
  type: str

class License(BaseModel):
  id: str
  tag: str
  key: str
  maxUses: int
  activations: list[str]
  expiryDate: str

ValidateElementType = Union[
  Table,
  Item,
  ClientItem,
  Kitchen,
  User,
  Session,
  Notification,
  Ticket,
  TicketItem,
  License
]