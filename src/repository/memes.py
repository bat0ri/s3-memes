from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio.session import AsyncSession

from repository.base import AsyncRepository
from repository.db import get_session

from domain.models.memes import Meme


class MemesRepository(AsyncRepository):

    entity = Meme


async def get_repository(
    session:  Annotated[AsyncSession, Depends(get_session)]
) -> MemesRepository:
    return MemesRepository(session=session)