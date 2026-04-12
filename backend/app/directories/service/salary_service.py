from core.db_postgres import async_session
from app.directories.dao.salary_dao import salary_dao


class SalaryConditionService:

  async def get_salary(self):
    async with async_session() as session:
      result = await salary_dao.get_all_salary(session)
      return result
    
  async def edit_salary(self, row_id: int, salary):
    async with async_session() as session:
      result = await salary_dao.update(session, row_id, **salary.model_dump())
      return result
    
salary_service: SalaryConditionService = SalaryConditionService()