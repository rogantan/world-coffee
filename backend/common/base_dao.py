from typing import TypeVar, Type, Generic
from sqlalchemy import select, update, func, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

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
    ) -> List[Model]:
        if not order_by:
            order_by = self.model.created_at
        else:
            order_by = getattr(self.model, order_by)
            if desc:
                order_by = order_by.desc()
        query = select(self.model).order_by(order_by).offset(offset).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def update(self, db: AsyncSession, model_id: int | str, **data: dict) -> Model:
        query = update(self.model).where(self.model.id == model_id).values(**data).returning(self.model)
        data = await db.execute(query)
        await db.commit()
        return data.scalars().one()
    
    async def select_one(self, db: AsyncSession, **filter: dict) -> Model | None:
        query = select(self.model).filter_by(**filter)
        result = await db.execute(query)
        return result.scalar()
    
    async def find_one_or_more(self, db: AsyncSession, **filter: dict) -> Model | None:
        query = select(self.model).filter_by(**filter)
        result = await db.execute(query)
        return result.scalars().one_or_none()
    
    async def find_by_id(self, db: AsyncSession, model_id: int | str) -> Model | None:
        query = select(self.model).filter_by(id=model_id)
        result = await db.execute(query)
        return result.scalar()
    
    async def add(self, db: AsyncSession, **data: Dict) -> Model:
        query = insert(self.model).values(**data)
        result = await db.execute(query.returning(self.model))
        await db.commit()
        return result.scalars().one()
    
    async def delete(self, db: AsyncSession, model_id: int | str) -> None:
        obj = await self.select_one(db, id=model_id)
        await db.delete(obj)
        await db.commit()

    async def get_all_with_filter(
        self,
        db: AsyncSession,
        order_by=None,
        **filter: dict,
    ) -> List[Model]:
        query = select(self.model).filter_by(**filter).order_by(order_by)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def find_all_with_filter(
        self,
        db: AsyncSession,
        **filter: dict,
    ) -> list[Model]:
        """Поиск всех записей по фильтру"""
        query = select(self.model).filter_by(**filter)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def insert_uncommit(
        self,
        db: AsyncSession,
        **data: dict,
    ) -> Model:
        """Добавление новой записи"""
        query = insert(self.model).values(**data).returning(self.model)
        data = await db.execute(query)
        return data.scalars().one()
    
    async def find_one_or_none(
        self,
        db: AsyncSession,
        **filter: dict,
    ) -> Model | None:
        """Поиск одной или никакой записи по фильтру"""
        query = select(self.model).filter_by(**filter)
        result = await db.execute(query)
        return result.scalars().one_or_none()
    
    async def delete_uncommit(
        self,
        db: AsyncSession,
        model_id: int | str,
    ) -> None:
        """Удаление записи по id"""
        obj = await self.select_one(db, id=model_id)
        await db.delete(obj)

    async def update_one_uncommit(
        self,
        db: AsyncSession,
        model_id: int | str,
        **data: dict,
    ) -> Model:
        """Обновление записи по id"""
        query = (
            update(self.model)
            .where(self.model.id == model_id)
            .values(**data)
            .returning(self.model)
        )
        data = await db.execute(query)
        await db.commit()
        return data.scalars().one()
    
    async def get_ids(
        self,
        db: AsyncSession,
        **filter: dict,
    ) -> list:
        """Получение списка id"""
        query = select(self.model.id).filter_by(**filter)
        result = await db.execute(query)
        return result.scalars().all()