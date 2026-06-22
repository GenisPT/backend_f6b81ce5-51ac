from fastapi.responses import FileResponse
from app.config.config import PERSISTENT_DATA_PATH

async def downloadIPA():
  return FileResponse(
    path=f'{PERSISTENT_DATA_PATH}app.ipa',
    filename="app.ipa",
    media_type="application/octet-stream"
  )

async def downloadAPK():
  return FileResponse(
    path=f'{PERSISTENT_DATA_PATH}app.apk',
    filename="app.apk",
    media_type="application/vnd.android.package-archive"
  )