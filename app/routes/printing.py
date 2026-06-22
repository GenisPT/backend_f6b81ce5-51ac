import base64
from fastapi import APIRouter
from datetime import datetime

from app.services.storage import load, dump, delete
from app.services.realtime import getRtime
from app.services.auth import validateOperation
from app.models.models import Print
from app.config.config import CLIENT_PRINTING_TOKEN, encodeESCPOS, checkTicketInDate, groupTicketItems

router = APIRouter()

@router.get("/queueprint/{sessionID}/{authToken}")
async def queuePrint(sessionID: str, authToken: str):
  if authToken != CLIENT_PRINTING_TOKEN:
    if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}
  collection = await load("printing")
  return collection

@router.post("/printallday/{dtime}/{paymentType}/{sessionID}/{authToken}")
async def printAllDay(dtime: str, paymentType: str, sessionID: str, authToken: str):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}
  tickets = await load("tickets")
  ticketItems = await load("ticketitems")
  now = datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S.%f")
  ids = [ti for ti in tickets if ti.paymentType == paymentType]
  ids = [ti.id for ti in ids if checkTicketInDate(now, ti)]
  if len(ids) == 0: return {"error": "There are no tickets generated on the specified date for the indicated payment type"}
  items = [it for it in ticketItems if it.ticketID in ids]
  now = now.strftime("%d/%m/%Y")
  esc = []

  esc.append(b'\x1b\x40')
  esc.append(b'\x1b\x74\x10')

  esc.append(b'\x1b\x61\x01')
  esc.append(b'\x1b\x21\x30')
  esc.append(b'\x1b\x45\x01')
  esc.append(encodeESCPOS("Restaurant 1\n"))
  esc.append(b'\x1b\x21\x00')
  esc.append(b'\x1b\x45\x00')
  esc.append(b'\x1b\x61\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\n')

  esc.append(b'\x1b\x61\x01')
  esc.append(encodeESCPOS(f"Paid with {paymentType}\n"))
  esc.append(b'\n')

  esc.append(b'\x1b\x61\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\x1b\x61\x01')
  esc.append(encodeESCPOS(f"{now}\n"))
  esc.append(b'\x1b\x61\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\n')

  esc.append(encodeESCPOS("Product            Price   Total\n"))
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\n')

  grandTotal = 0.0
  groupedItems = groupTicketItems(items)

  for item, quantity in groupedItems.items():
    if "1/2" in item[0]:
      name = item[0].replace("1", str(quantity))
    else:
      name = f"{quantity} x {item[0]}"
    
    name = name[:15] + "..." if len(name) >= 15 else name
    price = item[1] - (item[1] * (item[2] / 100))
    total = price * quantity
    grandTotal += total

    line_name = f"{name}"
    line_price = f"{price:.2f}".rjust(6)
    line_total = f"{total:.2f}".rjust(7)

    esc.append(encodeESCPOS(f"{line_name:<18}{line_price}{line_total}\n"))
  esc.append(b'\n')

  esc.append(b'\x1b\x61\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\x1b\x45\x01')
  esc.append(encodeESCPOS(f"{'TOTAL':<18}{'':6}{grandTotal:.2f}\n"))
  esc.append(b'\x1b\x45\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\x1b\x61\x01')
  esc.append(b'\n')

  esc.append(b'\x1b\x64\x05')
  esc.append(b'\x1d\x56\x00')

  pBytes = b"".join(esc)
  newPrint = Print(
    id="-",
    bytes=base64.b64encode(pBytes).decode("utf-8")
  )
  addition = await dump("printing", newPrint)
  if addition:
    await getRtime().notify("printing")
    return {"ok": "enqueued"}
  return {"error": "An error occurred while trying to add the print"}

@router.post("/enqueueprint/{ticketID}/{sessionID}/{authToken}")
async def enqueuePrinting(ticketID: str, sessionID: str, authToken: str):
  if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}
  tickets = await load("tickets")
  ticketItems = await load("ticketitems")
  ticket = [ti for ti in tickets if ti.id == ticketID][0]
  items = [it for it in ticketItems if it.ticketID == ticket.id]
  now = datetime.now().strftime("%d/%m/%Y %H:%M")
  esc = []

  esc.append(b'\x1b\x40')
  esc.append(b'\x1b\x74\x10')

  esc.append(b'\x1b\x61\x01')
  esc.append(b'\x1b\x21\x30')
  esc.append(b'\x1b\x45\x01')
  esc.append(encodeESCPOS("Restaurant 1\n"))
  esc.append(b'\x1b\x21\x00')
  esc.append(b'\x1b\x45\x00')
  esc.append(b'\x1b\x61\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\n')

  esc.append(b'\x1b\x61\x01')
  esc.append(encodeESCPOS("Street Two, 1\n"))
  esc.append(encodeESCPOS("Los Ángeles, CA (90002)\n"))
  esc.append(encodeESCPOS("@restaurant2\n"))
  esc.append(encodeESCPOS("(323) 123-4567\n"))
  esc.append(b'\n')

  esc.append(b'\x1b\x61\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\x1b\x61\x01')
  esc.append(encodeESCPOS(f"{now}\n"))
  esc.append(b'\x1b\x61\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\n')

  esc.append(encodeESCPOS("Product            Price   Total\n"))
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\n')

  grandTotal = 0.0
  groupedItems = groupTicketItems(items)

  for item, quantity in groupedItems.items():
    if "1/2" in item[0]:
      name = item[0].replace("1", str(quantity))
    else:
      name = f"{quantity} x {item[0]}"
    
    name = name[:15] + "..." if len(name) >= 15 else name
    price = item[1] - (item[1] * (item[2] / 100))
    total = price * quantity
    grandTotal += total

    line_name = f"{name}"
    line_price = f"{price:.2f}".rjust(6)
    line_total = f"{total:.2f}".rjust(7)

    esc.append(encodeESCPOS(f"{line_name:<18}{line_price}{line_total}\n"))
  esc.append(b'\n')

  esc.append(b'\x1b\x61\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\x1b\x45\x01')
  esc.append(encodeESCPOS(f"{'TOTAL':<18}{'':6}{grandTotal:.2f}\n"))
  esc.append(b'\x1b\x45\x00')
  esc.append(b'-' * 32 + b'\n')
  esc.append(b'\x1b\x61\x01')
  esc.append(b'\n')

  esc.append(encodeESCPOS(f"Ticket number {ticket.id}\n"))
  esc.append(encodeESCPOS(f"Table {ticket.tableName} ({ticket.persons} pers.)\n"))
  esc.append(encodeESCPOS(f"Paid with {ticket.paymentType.lower()}\n"))
  esc.append(b'\n')

  esc.append(encodeESCPOS("·· Thanks for your visit ··\n"))
  esc.append(encodeESCPOS(f"Attended by {ticket.waiterName}\n"))

  esc.append(b'\x1b\x64\x05')
  esc.append(b'\x1d\x56\x00')

  pBytes = b"".join(esc)
  newPrint = Print(
    id=ticket.id,
    bytes=base64.b64encode(pBytes).decode("utf-8")
  )
  addition = await dump("printing", newPrint)
  if addition:
    await getRtime().notify("printing")
    return {"ok": "enqueued"}
  return {"error": "An error occurred while trying to add the print"}

@router.delete("/dequeueprint/{ticketID}/{sessionID}/{authToken}")
async def dequeuePrinting(ticketID: str, sessionID: str, authToken: str):
  if authToken != CLIENT_PRINTING_TOKEN:
    if not await validateOperation(sessionID, authToken): return {"error": "Cannot validate access token"}
  deletion = await delete("printing", ticketID)
  if deletion:
    return {"ok": "dequeued"}
  return {"error": "An error occurred while trying to delete the print"}