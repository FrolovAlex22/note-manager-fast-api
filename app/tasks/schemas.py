from pydantic import BaseModel, Field




class TaskCreate(BaseModel):
    title: str = Field(max_length=50, description="Заголовок задачи")
    description: str = Field(max_length=200, description="Описание задачи")


class TaskUpdate(BaseModel):
    title: str = Field(max_length=50, description="Заголовок задачи")
    description: str = Field(max_length=200, description="Описание задачи")
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
