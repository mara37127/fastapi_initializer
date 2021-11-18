import models, schemas
from .authService import AuthService


class UserService:


    def get_user(self, user_id: int):
        user  = models.User
        try:
            value = user.get(user.id == user_id)
            return value.__data__
        except Exception as _:
            return None

    def get_user_by_username(self, username: str):
        user  = models.User
        try:
            value = user.get(user.username == username)
            return value.__data__
        except Exception as _:
            return None

    def get_users(self, skip: int = 0, limit: int = 100):
        user  = models.User
        try:
            values= list(user.select().offset(skip).limit(limit))
            return [user.__data__ for user in values]
        except Exception as _:
            return None

    def create_user(self, user: schemas.User):
        try:
            auth_service = AuthService()
            user.password = auth_service.encode_password(user.password)
            usr = models.User(**user.dict())
            usr.save()
            return user.username
        except Exception as _:
            return None