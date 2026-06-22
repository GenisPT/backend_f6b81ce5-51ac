from datetime import datetime

from app.models.models import Ticket, TicketItem

PERSISTENT_DATA_PATH = "data/"
ALLOWED_ORIGINS = ["*"]

CLIENT_PRINTING_TOKEN = "f87d8067-3e6e-4dcc-a6c1-3ee93a91fbfb-c9e68730-e5f5-48d4-a7f7-dee2a455916f-17f1a0f8-1aa6-4857-91c6-b3eebe139705-8da8df5c-0cc2-440e-b230-de473d4735a3"
CLIENT_UPDATING_TOKEN = "51871f7d-6088-4ee8-8d55-1f9b4f1456b3-52d0594b-3079-4fb3-b05c-18afdd992499-e2461e72-569c-4c02-8eb3-ab91cb4e5d26-7f67d705-6274-4081-aa25-e160aa04b2f9"

def encodeESCPOS(txt: str) -> bytes:
  return txt.encode('cp1252', errors='replace')

def checkTicketInDate(now: datetime, ticket: Ticket) -> bool:
  toCheck = datetime.strptime(ticket.closedDatetime, "%Y-%m-%d %H:%M:%S.%f")
  matchDay = toCheck.day == now.day
  matchMonth = toCheck.month == now.month
  matchYear = toCheck.year == now.year
  return matchDay and matchMonth and matchYear

def groupTicketItems(items: list[TicketItem]) -> dict[tuple[str, float, float], int]:
  grouped = {}
  for item in items:
    key = (item.name, item.price, item.discount)
    if grouped.get(key):
      grouped[key] += item.quantity
    else:
      grouped[key] = item.quantity
  return grouped