import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio.session import AsyncSession

from main import app
from repository.memes import MemesRepository
from domain.models.memes import Meme
from app.api.endpoints.memes import get_repository


async def mock_repository():
    mock_session = MagicMock(AsyncSession)
    repository = MemesRepository(session=mock_session)
    repository.get = AsyncMock(return_value=Meme(
        oid="1",
        title="MockData",
        content_type="png",
        content_size=100
    ))

    repository.all = AsyncMock(return_value=[])
    repository.insert = AsyncMock(return_value=Meme(
        oid="1",
        title="MockData",
        content_type="png",
        content_size=100
    ))
    repository.delete = AsyncMock(return_value=None)
    repository.update = AsyncMock(return_value=Meme(
        oid="1",
        title="MockDataUpdate",
        content_type="png",
        content_size=100
    ))
    return repository


app.dependency_overrides[get_repository] = mock_repository


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client
