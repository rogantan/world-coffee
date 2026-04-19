from core.db_postgres import async_session
from app.directories.dao.salary_dao import salary_dao
from app.directories.schema.salary_schema import SalarySchema
from uuid import UUID


class SalaryConditionService:
    
  async def edit_salary(self, row_id: UUID, salary: SalarySchema):
    async with async_session() as session:
      result = await salary_dao.update_salary(session, row_id, **salary.model_dump())
      return result
    
salary_service: SalaryConditionService = SalaryConditionService()