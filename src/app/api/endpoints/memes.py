from uuid import uuid4
from typing import Annotated
from fastapi import (
    APIRouter,
    UploadFile,
    HTTPException,
    Depends)
from sqlalchemy.ext.asyncio.session import AsyncSession

from storage.memes import (
    memes_s3,
    BUCKET_NAME,
    ENDPOINT_URL)
from domain.models.memes import Meme as MemeModel
from repository.memes import MemesRepository
from repository.memes import get_repository
from settings import MAX_FILE_SIZE, ALLOWED_IMAGE_TYPES


router = APIRouter(
    prefix="/memes",
    tags=["memes"],
)


async def validate_file(file: UploadFile) -> UploadFile:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type."
            )

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the limit of 5 MB."
            )

    return file


@router.post("/", status_code=201)
async def create_meme(
    session: Annotated[AsyncSession, Depends(get_repository)],
    file: Annotated[UploadFile, Depends(validate_file)],
    title: str,
        ):

    try:
        async with session.session.begin():
            inserted_meme = await session.insert(
                obj=MemeModel(
                    oid=str(uuid4()),
                    title=title,
                    content_type=file.content_type.split("/")[-1],
                    content_size=file.size
                )
            )
            content = await file.read()
            key = f'{inserted_meme.oid}.{inserted_meme.content_type}'
            await memes_s3.upload_file(
                file=content,
                key=key
            )
    except HTTPException:
        raise HTTPException(
            status_code=400,
            detail="Мем не загружен"
        )

    return {
        "meme": inserted_meme.to_dict(),
        "url": f"{ENDPOINT_URL}/{BUCKET_NAME}/{key}"
    }


@router.get("/{id}")
async def get_meme_by_id(
    id: str,
    session: Annotated[AsyncSession, Depends(get_repository)],
):
    try:
        meme = await session.get(id)
        key = f'{meme.oid}.{meme.content_type}'

        return {
            "meme": meme.to_dict(),
            "url": f"{ENDPOINT_URL}/{BUCKET_NAME}/{key}",
            }
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Мем не найден."
        )


async def paginator_commons(page: int = 1, paginator: int = 10):
    return {
        "page": page,
        "paginator": paginator
    }


@router.get("/", status_code=200)
async def get_memes(
    session: Annotated[AsyncSession, Depends(get_repository)],
    commons: Annotated[dict, Depends(paginator_commons)]
):
    try:
        memes = await session.all(
            page=commons["page"],
            paginator=commons["paginator"]
        )
        return {
            "memes": [meme.to_dict() for meme in memes]
        }
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Мемы не найдены {e}"
        )


@router.put("/{id}")
async def update_meme_by_id(
    id: str,
    session: Annotated[AsyncSession, Depends(get_repository)],
    file: Annotated[UploadFile, Depends(validate_file)],
    title: str = None,
):

    try:
        async with session.session.begin():
            meme = await session.get(id)

            if meme is None:
                raise HTTPException(
                    status_code=404,
                    detail="Нет мема с таким идентификатором."
                )

            meme.title = title
            if file.content_type.split("/")[-1] != meme.content_type:
                await memes_s3.delete_file(
                    key=f'{meme.oid}.{meme.content_type}'
                )
                meme.content_type = file.content_type.split("/")[-1]

            meme.content_size = file.size
            await memes_s3.upload_file(
                file=await file.read(),
                key=f'{meme.oid}.{meme.content_type}'
            )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Не удалось обновить мем"
        )

    return {
        "Файл загружен как": f'{meme.oid}.{meme.content_type}',
        "Исходник": file.filename,
        "Размер": f'{meme.content_size // 1024} KB',
        "Тип": meme.content_type,
        "Идентификатор": meme.oid
    }


@router.delete("/{id}")
async def delete_meme_by_id(
    id: str,
    session: Annotated[AsyncSession, Depends(get_repository)],
):
    try:
        meme = await session.get(id)
        if meme is None:
            raise HTTPException(
                status_code=404,
                detail="Нет мема с таким идентификатором."
            )

        await memes_s3.delete_file(key=f'{id}.{meme.content_type}')
        await session.delete(id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Мем не удален. {e}"
        )

    return {
        "message": f"Мем {id} удален."
    }
