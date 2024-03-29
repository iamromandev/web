import requests
from loguru import logger
from rest_framework.views import exception_handler


class CircularQueue:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.array = [None] * max_size
        self.front = 0
        self.rear = 0
        self.size = 0

    def enqueue(self, item):
        if self.size >= self.max_size:
            raise Exception("Queue is full")

        self.array[self.rear] = item
        self.rear = (self.rear + 1) % self.max_size
        self.size += 1
        return self

    def dequeue(self):
        if self.size == 0:
            raise Exception("Underflow")

        item = self.array[self.front]
        self.array[self.front] = None
        self.front = (self.front + 1) % self.max_size
        self.size -= 1
        return item

    def peek(self):
        if self.size == 0:
            raise Exception("Underflow")

        return self.array[self.front]

    def iterate(self):
        self.enqueue(self.dequeue())


def generic_exception_handler(exc, context):
    logger.exception(exc)
    response = exception_handler(exc, context)
    if response is not None:
        response.data["status_code"] = response.status_code
    return response


class ApiClient:
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(
            {
                "content-type": "application/json; charset=utf-8",
                "accept": "application/json; charset=utf-8",
            }
        )

    @property
    def session(self) -> requests.Session:
        return self._session

    def get(self, url: str, params: dict = {}) -> dict:
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]
