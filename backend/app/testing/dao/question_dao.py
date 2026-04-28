from common.base_dao import BaseDao
from core.db_postgres import AsyncSession
from app.testing.model.choice import Choice
from app.testing.model.question import Question
from app.testing.model.user_answer import UserAnswer
from sqlalchemy import select, update, delete, func

class QuestionDao(BaseDao[Question]):
  pass

question_dao: QuestionDao = QuestionDao(Question)