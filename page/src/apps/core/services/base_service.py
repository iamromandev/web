from typing import Any

from loguru import logger


class BaseService:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def log_info(self, message: str) -> None:
        logger.info(message)

    def log_error(self, error: Any, exc_info: bool = True) -> None:
        logger.error(error, exc_info=exc_info)
