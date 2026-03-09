"""
Realtime communication service.

Allows clients to subscribe through WebSocket connections
to receive notifications whenever a data collection changes.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.config import ALLOWED_ORIGINS

router = APIRouter()
# List of active WebSocket connections subscribed to updates
realtimeSubscriptions: list[WebSocket] = []

"""
WebSocket endpoint used by clients to subscribe
to data change notifications.
"""
@router.websocket("/ws")
async def realtime(websocket: WebSocket):
  origin = websocket.headers.get("origin")
  if origin is not None and origin not in ALLOWED_ORIGINS:
    await websocket.close(code=1008)
    return

  await websocket.accept()
  realtimeSubscriptions.append(websocket)
  print("New client connected to Realtime Service")
  try:
    while True:
      await websocket.receive_text()
  except WebSocketDisconnect:
    realtimeSubscriptions.remove(websocket)
    print("Client disconnected from Realtime Service")

"""
Notifies all connected WebSocket clients that a
specific collection has been modified so they can
refresh their data.
"""
async def notifyChanges(collectionID: str):
  erroredSubscriptions = []
  for subs in realtimeSubscriptions:
    try:
      await subs.send_text(collectionID)
    except:
      erroredSubscriptions.append(subs)
  for subs in erroredSubscriptions:
    # If a connection fails, marl it to be removed
    realtimeSubscriptions.remove(subs)
  print("Sent '", collectionID, "' changes message to all subscribers", sep="")