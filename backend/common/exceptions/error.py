from fastapi import HTTPException, status


class APIException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
        
class ForbiddenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Доступ запрещен"

class RoleNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Роль с таким названием не найдена"

class UserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"

class RetailStoreIdNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Точка продаж с таким ID не найдена"

class PaymentPurposeIdNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Назначение платежа не найдено"

class TestNoActiveException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Тест еще не открыт или уже закрыт"

class TestAlreadyPassedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Тест уже был пройден"

class NoAnswerToQuestionException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "На какой-то из вопросов не выбрано ни одного ответа"

class AnswerOptionNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Вариант ответа c таким ID не найден или отсутствует в тесте"

class TestNameAlreadyExistsException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Тест с таким именем уже существует"

class TestCannotBeEditedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Тест нельзя изменить"

class InvalidOrderByValueException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Некорректное значение сортировки"

class TestNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Тестирование не найдено"

class QuestionNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Вопрос не найден"

class UnprocessableEntity(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Фактический остаток меньше, чем сумма продаж"

class CustomInventoryItemNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Позиция инвентаризации с таким ID не найдена"

class ActualBalanceLessThanSaleSumException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Фактический остаток меньше, чем сумма продаж"