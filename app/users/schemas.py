from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(
        min_length=3, max_length=50, description="Имя, от 3 до 50 символов"
    )
    password_hash: str = Field(
        min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )


class UserResponse(BaseModel):
    username: str


class UserAuth(BaseModel):
    username: str = Field(description="username пользователя")
    password: str = Field(
        min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )


class IdItem(BaseModel):
    id: str = Field(description="Идентификационный номер сервиса")
