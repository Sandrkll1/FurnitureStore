import os
from urllib.parse import unquote

import aiofiles
from fastapi import APIRouter, HTTPException, Query
from starlette.responses import FileResponse, StreamingResponse

from api.data.controller import get_media_type

router = APIRouter(prefix="/data", tags=["data", "images"])


@router.get("/image")
async def download_image(image_path: str = Query(...)):
    decoded_image_path = unquote(image_path)

    if not os.path.exists(decoded_image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(decoded_image_path)


@router.get("/stream")
async def stream_file(image_path: str = Query(...)):
    decoded_image_path = unquote(image_path)

    if not os.path.exists(decoded_image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    async def iter_file():
        async with aiofiles.open(decoded_image_path, mode="rb") as file_like:
            chunk = await file_like.read(1024)
            while chunk:
                yield chunk
                chunk = await file_like.read(1024)

    return StreamingResponse(iter_file(), media_type=get_media_type(decoded_image_path))

