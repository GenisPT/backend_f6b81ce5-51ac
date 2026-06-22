import asyncio
import logging
import redis.asyncio as rclient

from fastapi import WebSocket

rtimeLogger = logging.getLogger(__name__)

class Realtime:
  def __init__(self):
    self.subscriptions: set[WebSocket] = set()
    self.redis: rclient.Redis | None = None
    self.listener: asyncio.Task | None = None
  
  async def redisConnect(self, redis: rclient.Redis):
    self.redis = redis
    self.listener = asyncio.create_task(self._redisListener())
  
  async def _redisListener(self):
    if not self.redis:
      return
    
    pubsub = self.redis.pubsub()
    await pubsub.psubscribe("realtime:*")

    try:
      async for msg in pubsub.listen():
        if msg["type"] == "pmessage" and msg.get("data"):
          try:
            collection = msg["data"].decode() if isinstance(msg["data"], bytes) else str(msg["data"])
            errored = []
            for subs in list(self.subscriptions):
              try:
                await subs.send_text(collection)
              except Exception:
                errored.append(subs)
              
              for subs in errored:
                await self.unsubscribe(subs)
          except Exception as e:
            rtimeLogger.error(f"[!] Realtime error: {e}")
    except asyncio.CancelledError:
      pass
    except Exception as e:
      rtimeLogger.error(f"[!] Realtime error: {e}")
    finally:
      await pubsub.aclose()
  
  async def subscribe(self, ws: WebSocket):
    await ws.accept()
    self.subscriptions.add(ws)
    rtimeLogger.info(f"[+] Client connected to Realtime | Subscriptions: {len(self.subscriptions)}")
  
  async def unsubscribe(self, ws: WebSocket):
    self.subscriptions.discard(ws)
    rtimeLogger.info(f"[-] Client desconnected from Realtime | Subscriptions: {len(self.subscriptions)}")
  
  async def notify(self, collectionID: str):
    if not self.redis:
      return
    
    channel = f"realtime:{collectionID}"
    await self.redis.publish(channel, collectionID)
    rtimeLogger.info(f"[i] Notified changes of collection: {collectionID}")