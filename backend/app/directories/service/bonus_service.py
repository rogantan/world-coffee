from core.db_postgres import async_session
from app.directories.dao.bonus_dao import bonus_dao
from app.directories.schema.bonus_schema import BonusSchema


class BonusService:

  async def get_bonuses(self):
    async with async_session() as session:
      result = await bonus_dao.get_all(session)
      return result
  
  async def create_bonus(self, bonus: BonusSchema):
    async with async_session() as session:
      result = await bonus_dao.add(session, **bonus.model_dump())
      return result
    
  async def edit_bonus(self, row_id: int, bonus: BonusSchema):
    async with async_session() as session:
      result = await bonus_dao.update(session, row_id, **bonus.model_dump())
  
bonus_service: BonusService = BonusService()