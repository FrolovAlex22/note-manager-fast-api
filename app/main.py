from contextlib import asynccontextmanager
import logging.config

from fastapi import FastAPI
import uvicorn

from database.database import create_models, delete_models
from config.logging_settings import logging_config
from users.router import router as router_users
from config.config import settings


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_models()
    logger.info("База очищена")
    await create_models()
    logger.info("База готова")
    yield
    logger.info("Выключение")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home_page():
    return {"message": "Привет, все работает!"}


app.include_router(router_users)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.MAIN.HOST,
        port=settings.MAIN.PORT,
        reload=True,
    )
