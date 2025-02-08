import logging

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_filter import FilterDepends

from filters import TaskFilter
from dependencies import get_current_user
from tasks.dao import TasksDAO
from tasks.schemas import TaskCreate, TaskResponse, TaskUpdate
from database.models import User


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
        "/create",
        status_code=status.HTTP_201_CREATED,
        response_model=TaskResponse
    )
async def create_task(
    task_in: TaskCreate, user: User = Depends(get_current_user)
):
    check = await TasksDAO.find_one_by_title_and_user(
        title=task_in.title,
        owner_id=user.id
    )
    if check:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Задача уже существует"
        )
    task_dict = task_in.model_dump()
    task_dict["owner_id"] = user.id
    task = await TasksDAO.add(task_dict)
    logger.info(f"Пользователь: {user} добавил задачу {task.title}")
    return task


@router.get(
        "/my_tasks",
        status_code=status.HTTP_200_OK,
        response_model=list[TaskResponse])
async def get_my_tasks(
    current_user: User = Depends(get_current_user),
    task_filter: TaskFilter = FilterDepends(TaskFilter)
):
    tasks = await TasksDAO.find_all_by_user(
        user_id=current_user.id, filter=task_filter
    )
    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Добавьте задачи"
        )
    logger.info(f"Пользователь: {current_user} получил список задач")
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_id(
    task_id: int,
    user: User = Depends(get_current_user),
):
    task = await TasksDAO.find_one_by_id_and_user(task_id, user.id)
    logger.info(f"Пользователь: {user} получил задачу {task.title}")
    if task is None:
        logger.info("Задача не найдена")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.patch("/{task_id}/update", response_model=TaskResponse)
async def update_task(
    task_id: int,
    updarted_dict: TaskUpdate,
    user: User = Depends(get_current_user),
):
    task = await TasksDAO.find_one_by_id_and_user(task_id, user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        updarted_task = updarted_dict.model_dump()
        task = await TasksDAO.update(updarted_task, task_id)
        logger.info(f"Пользователь: {user} обновил задачу {task.title}")
        return task
    except Exception as e:
        logger.info(f"При обновлении задачи произошла ошибка: {e}")


@router.delete("/delete/{task_id}")
async def delete_task_by_id(
    task_id: int,
    user: User = Depends(get_current_user),
):
    task = await TasksDAO.find_one_or_none_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this task"
        )
    try:
        await TasksDAO.delete(task_id)
        logger.info(f"Пользователь: {user} удалил задачу {task.title}")
        return {"message": f"Task {task.title} deleted successfully"}
    except Exception as e:
        logger.info(f"При удалении задачи произошла ошибка: {e}")
