from typing import TypeVar, Type, Generic
from sqlalchemy import select, update, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")

class BaseDao(Generic[Model]):

    def __init__(self, model: Type[Model]):
        self.model = model

    async def get_all(
        self,
        db: AsyncSession,
        offset: int = 0,
        limit: int = None,
        order_by: str = None,
        desc: bool = False
    ) -> list[Model]:
        if not order_by:
            order_by = self.model.created_at
        else:
            order_by = getattr(self.model, order_by)
            if desc:
                order_by = order_by.desc()
        query = select(self.model).order_by(order_by).offset(offset).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    