from common.base_dao import BaseDao
from app.directories.model.bonus import Bonus

class BonusDao(BaseDao[Bonus]):
  pass

bonus_dao: BonusDao = BaseDao(Bonus)