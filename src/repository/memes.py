from repository.base import AsyncRepository

from domain.models.memes import Meme


class MemesRepository(AsyncRepository):

    entity = Meme
