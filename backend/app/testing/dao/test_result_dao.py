from typing import List
from common.base_dao import BaseDao
from app.testing.model.test import Test
from core.db_postgres import AsyncSession
from app.testing.model.choice import Choice
from app.testing.model.question import Question
from app.testing.model.test_result import TestResult
from sqlalchemy import select, update, delete, func

class TestResultDao(BaseDao[TestResult]):
  pass

test_result_dao: TestResultDao = TestResultDao(TestResult)