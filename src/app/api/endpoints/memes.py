from typing import Annotated
from fastapi import (
    APIRouter,
    UploadFile,
    HTTPException,
    Depends)
from fastapi.responses import FileResponse, StreamingResponse, Response

from sqlalchemy.ext.asyncio.session import AsyncSession

from pydantic import Field

from storage.memes import memes_s3
from app.api.schemas.memes import validate_file
from domain.entities.memes import Meme
from repository.memes import MemesRepository
from repository.db import get_session


router = APIRouter(
    prefix="/memes",
    tags=["memes"],
)


@router.post("/")
async def post_meme(
    session: Annotated[AsyncSession, Depends(get_session)],
    file: UploadFile = Depends(validate_file),
    title: str = None,
        ):

    file_content = await file.read()
    content_type = file.content_type.split("/")[-1]

    try:
        async with session.begin():
            meme = Meme(
                title=title,
                content_type=content_type,
                content_size=len(file_content)
            )
            await MemesRepository(session).insert(meme.to_model())
            await memes_s3.upload_file(
                file_content,
                f'{title}_{meme.oid}.{content_type}'
                )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Не удалось загрузить мем."
        )

    return {
        "Файл загружен как": f'{title}_{meme.oid}.{content_type}',
        "Исходник": file.filename,
        "Размер": f'{len(file_content) // 1024} KB',
        "Тип": content_type,
        "Идентификатор": meme.oid
    }


@router.get("/open/{id}")
async def get_meme(
    id: str,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    try:
        meme = await MemesRepository(session).get(id)
        if not meme:
            raise HTTPException(
                status_code=404,
                detail="Мем не найден."
            )
        file_key = f'{meme.title}_{meme.oid}.{meme.content_type}'
        response = await memes_s3.get_file(file_key)
        return StreamingResponse(
            response["Body"],
            media_type="image/png"
        )
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Мем не найден."
        )


@router.get("/{id}")
async def get_meme_by_id(
    id: str,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    try:
        meme = await MemesRepository(session).get(id)
        if not meme:
            raise HTTPException(
                status_code=404,
                detail="Мем не найден."
            )
        return {
            "meme": meme.to_dict(),
        }
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Мем не найден."
        )


@router.get("/")
async def get_memes(
    session: Annotated[AsyncSession, Depends(get_session)],
    page: int = 1,
    paginator: int = 10,
):
    try:
        memes = await MemesRepository(session).all(
            page=page,
            paginator=paginator
        )
        return {
            "memes": [meme.to_dict() for meme in memes]
        }
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Мемы не найдены."
        )
