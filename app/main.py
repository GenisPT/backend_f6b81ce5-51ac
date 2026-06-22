import asyncio
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config.config import ALLOWED_ORIGINS
from app.tasks import taskCheckSessions
from app.routes import elements, auth, licenses, printing, updates
from app.services.storage import initRedis, getRedis
from app.services.realtime import router as rtime_router, initRtime, getRtime

@asynccontextmanager
async def lifespan(app: FastAPI):
  ## Recurrent Tasks ##
  taskSessions = asyncio.create_task(taskCheckSessions(
    interval=60.0
  ))

  ## Initalizations ##
  initRedis("redis://localhost:6379", decodeResponses=True)
  initRtime()
  await getRtime().redisConnect(getRedis())

  yield

  ## Cancel Recurrent Tasks ##
  taskSessions.cancel()

  ## Deinitializations ##
  await getRedis().aclose()
  if getRtime().listener is not None:
    getRtime().listener.cancel()

app = FastAPI(
  lifespan=lifespan,
  default_response_class=ORJSONResponse
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=ALLOWED_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(elements.router)
app.include_router(auth.router)
app.include_router(licenses.router)
app.include_router(printing.router)
app.include_router(updates.router)
app.include_router(rtime_router)

@app.get("/ping")
def ping():
  return {
    "api_ver": "1.0.0",
    "app_ver": "0.1.17",
    "hist_ver": {
      "0.0.1": True,
      "0.0.2": True,
      "0.0.12": True,
      "0.0.29": True,
      "0.1.0": False
    }
  }