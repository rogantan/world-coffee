from utils.date_formatter import ms_date_to_datetime
from common.base_dao import BaseDao
from app.reports.model.retail_store import RetailStore
from core.db_postgres import AsyncSession
from sqlalchemy import select
from app.directories.model.salary import SalaryCondition

class RetailStoreDao(BaseDao[RetailStore]):
    
    async def get_retail_stores(self, db: AsyncSession):
        query = select(RetailStore.id, RetailStore.name, RetailStore.archived, SalaryCondition.salary_per_shift).join(SalaryCondition, RetailStore.id == SalaryCondition.retail_store_id)
        result = await db.execute(query)
        return result.mappings().all()
    
    def get_id_from_object(self, entity: dict, odject_name: str) -> str | None:
        """Получение id из href ссылки"""
        obj = entity.get(odject_name)
        if not obj:
            return

        href = obj.get("meta", {}).get("href")
        return href.split("/")[-1]
    
    async def add_new_entity(self, db, entity):
        await self.insert_uncommit(
            db,
            id=entity.get("id"),
            name=entity.get("name"),
            store_id=self.get_id_from_object(entity, "store"),
            archived=entity.get("archived"),
            ms_updated=ms_date_to_datetime(entity.get("updated")),
        )
        await db.commit()
    
    async def update_entity(self, db, entity):
        await self.update(
            db,
            entity.get("id"),
            name=entity.get("name"),
            store_id=self.get_id_from_object(entity, "store"),
            archived=entity.get("archived"),
            ms_updated=ms_date_to_datetime(entity.get("updated")),
        )

    async def delete_entity(self, db, entity_id):
        await self.update(db, entity_id, archived=True)

retail_store_dao: RetailStoreDao = RetailStoreDao(RetailStore)