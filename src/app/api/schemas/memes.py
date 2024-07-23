from settings import MAX_FILE_SIZE, ALLOWED_IMAGE_TYPES
from fastapi import UploadFile, HTTPException


async def validate_file(file: UploadFile):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type."
            )

    file_size = await file.read()
    if len(file_size) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the limit of 5 MB."
            )
    await file.seek(0)
    return file
