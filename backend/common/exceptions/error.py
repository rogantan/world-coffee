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