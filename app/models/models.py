from pydantic import BaseModel, Field
from typing import Union, Literal, Annotated

# ===== Restaurant ===== #
class Table(BaseModel):
  type: Literal["table"] = "table"
  id: str
  name: str
  status: str
  persons: int
  waitersID: str
  waitersName: str

class Item(BaseModel):
  type: Literal["item"] = "item"
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
  type: Literal["clientitem"] = "clientitem"
  id: str
  name: str
  isKitchen: bool
  category: str
  price: float
  metrics: int

class Kitchen(BaseModel):
  type: Literal["kitchen"] = "kitchen"
  id: str
  status: str

# ===== Comandes ===== #
class Ticket(BaseModel):
  type: Literal["ticket"] = "ticket"
  id: str
  tableName: str
  waiterName: str
  openedDatetime: str
  closedDatetime: str
  persons: int
  paid: float
  paymentType: str

class TicketItem(BaseModel):
  type: Literal["ticketitem"] = "ticketitem"
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

# ===== Autenticació ===== #
class User(BaseModel):
  type: Literal["user"] = "user"
  id: str
  password: str
  name: str
  surname: str
  roles: list[str]

class Session(BaseModel):
  type: Literal["session"] = "session"
  id: str
  user: str
  expiryDate: str

# ===== Sistema ===== #
class Group(BaseModel):
  type: Literal["group"] = "group"
  collectionID: str
  elements: list[dict]

class Notification(BaseModel):
  type: Literal["notification"] = "notification"
  id: str
  user: str
  typeNoti: str

class License(BaseModel):
  type: Literal["license"] = "license"
  id: str
  tag: str
  key: str
  maxUses: int
  activations: list[str]
  expiryDate: str

class Print(BaseModel):
  type: Literal["print"] = "print"
  id: str
  bytes: str

ValidateElementType = Annotated[
  Union[
    Table,
    Item,
    ClientItem,
    Kitchen,
    User,
    Session,
    Notification,
    Ticket,
    TicketItem,
    License,
    Print,
    Group
  ],
  Field(discriminator="type")
]