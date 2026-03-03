from enum import Enum

class Status(Enum):
    SUCCESS = "Обновление успешно завершено"
    IN_PROGRESS = "Обновление выполняется"
    ERROR = "Произошла ошибка при обновлении"