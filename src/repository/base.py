"""
    Repository interface and SQLAlchemy adapter w/ this interface.
"""
from sqlalchemy import (
    select,
    delete as sqlalchemy_delete,
    update as sqlalchemy_update
)
from functools import wraps


class AsyncBaseRepository:
    """
        Interface for working with database.
    """
    entity = NotImplementedError

    async def insert(self, obj):
        raise NotImplementedError

    async def get(self, id):
        raise NotImplementedError

    async def all(self, limit=100, offset=0, sorted=None):
        raise NotImplementedError

    async def update(self, id, obj):
        raise NotImplementedError

    async def delete(self, id):
        raise NotImplementedError

    async def drop(self):
        raise NotImplementedError


def transaction(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            await self.session.rollback()
            raise e
    return wrapper


class AsyncRepository(AsyncBaseRepository):

    def __init__(self, session):
        self.session = session

    @transaction
    async def insert(self, obj):
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    @transaction
    async def get(self, id):
        query = select(self.entity).where(self.entity.oid == id)
        result = await self.session.execute(query)
        return result.scalars().first()

    @transaction
    async def all(self, page=1, paginator=100, sorted=None):
        query = select(self.entity).limit(paginator).offset(
            (page - 1) * paginator
            )
        if sorted:
            query = query.order_by(sorted)
        result = await self.session.execute(query)
        return result.scalars().all()

    @transaction
    async def update(self, id, obj):
        query = sqlalchemy_update(self.entity).where(
            self.entity.oid == id
            ).values(**obj)
        await self.session.execute(query)
        await self.session.flush()
        return await self.get(id)

    @transaction
    async def delete(self, id):
        query = sqlalchemy_delete(self.entity).where(self.entity.id == id)
        await self.session.execute(query)
        await self.session.flush()
        return True

    @transaction
    async def drop(self):
        await self.session.execute(sqlalchemy_delete(self.entity))
        await self.session.flush()
        return True
