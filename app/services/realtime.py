import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.config.config import ALLOWED_ORIGINS
from app.config.realtime import Realtime

router = APIRouter()
_rtime: Realtime | None = None

def initRtime():
  global _rtime
  _rtime = Realtime()

def getRtime() -> Realtime:
  global _rtime
  return _rtime

@router.websocket("/ws")
async def realtime(ws: WebSocket):
  origin = ws.headers.get("origin")
  if origin is not None and origin not in ALLOWED_ORIGINS:
    await ws.close(code=1008)
    return

  await _rtime.subscribe(ws)

  try:
    while True:
      await asyncio.sleep(30)
      try:
        await ws.send_text("connCheck")
      except:
        break
  except WebSocketDisconnect:
    await _rtime.unsubscribe(ws)
  except Exception as e:
    await _rtime.unsubscribe(ws)
    print(f"[!] An error occurred regarding Realtime: {e}")