from common.base_dao import BaseDao
from app.admin.model.salary_increase import SalaryIncrease


class SalaryIncreaseDao(BaseDao[SalaryIncrease]):
  pass

salary_increase_dao: SalaryIncreaseDao = SalaryIncreaseDao(SalaryIncrease)