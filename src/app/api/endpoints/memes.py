from fastapi import (
    APIRouter,
    UploadFile,
    HTTPException,
    Depends)

from storage.memes import memes_s3
from app.api.schemas.memes import validate_file


router = APIRouter(
    prefix="/memes",
    tags=["memes"],
)


@router.post("/")
async def post_meme(
    file: UploadFile = Depends(validate_file),
    title: str = None
        ):
    if not title:
        raise HTTPException(
            status_code=400,
            detail="Название не может быть пустым."
        )

    file_content = await file.read()
    content_type = file.content_type.split("/")[-1]
    object_name = f"{title}.{content_type}"

    await memes_s3.upload_file(file_content, object_name)

    return {
        "Файл загружен как": object_name,
        "Исходник": file.filename,
        "Размер": f'{len(file_content) / 1024} KB'
    }
