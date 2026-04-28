"""Модуль pydantic-схем для работы с тестами"""

from datetime import datetime, date
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, Field, field_validator, validator

# from app.schemas.pagination import SPagination


def delete_timezone(date: datetime):
  """Приведение даты к нужному формату без таймзоны"""
  date = date.replace(tzinfo=None)
  return date


def validate_questions(questions: list):
  """Валидация списка вопросов"""
  if not questions:
    raise ValueError("Ожидается хотя бы один вопрос")

  return questions


def validate_choices(choices: list):
  """Валидация списка вариантов ответа"""
  if not choices:
    raise ValueError("Ожидается хотя бы один вариант ответа")

  for answer_option in choices:
    if answer_option.is_correct:
      return choices

  raise ValueError("Необходим хотя бы один верный вариант ответа")


class STest(BaseModel):
  """Модель теста со всеми полями из БД"""

  id: int
  name: str
  date_from: datetime
  date_to: datetime
  result_resets: bool


class SQuestion(BaseModel):
  """Модель вопроса со всеми полями из БД"""

  id: int
  text: str


class SAnswerOption(BaseModel):
  """Модель варианта ответа со всеми полями из БД"""

  id: int
  text: str
  is_correct: bool


class STestForModification(BaseModel):
  """Модель теста для создания/изменения"""

  name: str
  date_from: datetime
  date_to: datetime
  questions: list

  @validator("date_to")
  @classmethod
  def date_validator(cls, date_to: datetime, values):
    """Валидация даты начала теста"""
    if delete_timezone(date_to) < values["date_from"]:
      raise ValueError("Дата начала теста не может быть позже даты окончания")
    return date_to

  @field_validator("date_from", "date_to")
  @classmethod
  def date_format(cls, date: datetime):
    """Приведение даты к нужному формату без таймзоны"""
    return delete_timezone(date)

  @field_validator("questions")
  @classmethod
  def questions_validator(cls, questions: list):
    """Валидация списка вопросов"""
    return validate_questions(questions)

  model_config = {"from_attributes": True}


class SQuestionForModification(BaseModel):
  """Модель вопроса для создания/изменения"""

  text: str
  choices: list

  @field_validator("choices")
  @classmethod
  def choices_validator(cls, choices: list):
    """Валидация списка вариантов ответа"""
    return validate_choices(choices)

  model_config = {"from_attributes": True}


class SCreateAnswerOption(BaseModel):
  """Модель варианта ответа для создания теста"""

  text: str
  is_correct: bool


class SCreateQuestion(SQuestionForModification):
  """Модель вопроса для создания теста"""

  choices: list[SCreateAnswerOption]


class SCreateTest(STestForModification):
  """Модель теста для создания"""

  questions: list[SCreateQuestion]


class SUpdateAnswerOption(SAnswerOption):
  """Модель варианта ответа для обновления теста"""

  id: int | None = None
  model_config = {"from_attributes": True}


class SUpdateQuestion(SQuestionForModification):
  """Модель вопроса для обновления теста"""

  id: int | None = None
  choices: list[SUpdateAnswerOption]


class SUpdateTest(STestForModification):
  """Модель теста для обновления"""

  questions: list[SUpdateQuestion]


class STestForList(STest):
  """Модель теста c дополнительной информацией о том,
  был ли пройден тест"""

  was_passed: bool
  is_active: bool

class SQuestionWithAnswerOptions(SQuestion):
  """Модель вопроса с вариантами ответов"""

  choices: list[SAnswerOption]


class STestWithQuestionsAndAnswers(STest):
  """Модель теста с вопросами и ответами"""

  questions: list[SQuestionWithAnswerOptions]


class SAnswerOptionText(BaseModel):
  """Модель варианта ответа c id и текстом"""

  id: int
  text: str

  model_config = {"from_attributes": True}


class SQuestionForPassing(SQuestion):
  """Модель вопроса для прохождения теста"""

  multiple_answer: bool = False
  choices: list[SAnswerOptionText]

  model_config = {"from_attributes": True}


class STestForPassing(STest):
  """Модель теста для прохождения"""

  questions: list[SQuestionForPassing]

  model_config = {"from_attributes": True}


class SDate(BaseModel):
  """Модель даты для отчета о результатах тестирования"""

  date_from: date
  date_to: date
  short_date: str
  displayed_date: str


class SBestEmployeeRow(BaseModel):
  """Модель строки отчета лучший сотрудник в одном месяце по сотр."""

  date: date
  test_rank: int
  avg_check_dinamic: str | None
  avg_check_rank: int
  total_points: int
  total_rank: int

  model_config = {"from_attributes": True}


class SAnswerOptionResult(SAnswerOption):
  """Модель варианта ответа для результата"""

  correct_answer: bool
  selected: bool


class SQuestionResult(SQuestion):
  """Модель результата вопроса"""

  multiple_answer: bool = False
  correct_answers: bool
  color: str
  choices: list[SAnswerOptionResult]


class STestResult(BaseModel):
  """Модель теста с вопросами и ответами"""

  id: int
  name: str
  date_from: datetime
  date_to: datetime
  questions: list[SQuestionResult]


class STestInMonth(BaseModel):
  """Модель теста в месяце"""

  test_id: int
  user_id: UUID
  name: str
  finish_date: datetime
  result: str


class TestFilter(BaseModel):
  date_from: date
  date_to: date
  date_order_by: datetime | None = None
  order_by: str | None = None
  desc: bool = False
