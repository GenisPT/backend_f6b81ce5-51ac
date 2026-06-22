import asyncio
from datetime import datetime

from app.services.storage import load, delete
from app.services.realtime import getRtime


async def taskCheckSessions(interval: float):
  taskTime = asyncio.get_event_loop().time()
  sessions = await load("sessions")

  while True:
    for session in sessions:
      date = datetime.now()
      expiryDate = datetime.strptime(session.expiryDate, "%Y-%m-%d %H:%M:%S.%f")

      if date > expiryDate:
        deletion = await delete("sessions", session.id)
        if deletion:
          await getRtime().notify("sessions")
    
    taskTime += interval
    sleepTime = taskTime - asyncio.get_event_loop().time()

    if sleepTime > 0:
      await asyncio.sleep(sleepTime)
    else:
      taskTime = asyncio.get_event_loop().time()