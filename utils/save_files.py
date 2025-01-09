import os
import uuid

import aiofiles
from fastapi import HTTPException, UploadFile, status


async def save_image(image: UploadFile, directory: str) -> str:
    if image.filename.split(".")[-1].lower() not in ['jpeg', 'png', 'jpg', 'gif']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image type")

    return await save_file(image, directory)


async def save_file(file: UploadFile, directory: str) -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(directory, filename)

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return file_path


async def save_media_files(files: list[UploadFile], directory: str) -> list[str]:
    media_files = []
    if not os.path.exists(directory):
        os.makedirs(directory)

    for file in files:
        media_files.append(await save_file(file, directory))
    return media_files
