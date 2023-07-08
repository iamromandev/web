import time
import random
from urllib.error import HTTPError

from loguru import logger
from wordnik import swagger, WordApi

from config.settings import WORDNIK_API_KEYS
from apps.core.libs import (
    CircularQueue,
    ApiClient,
    SingletonMeta,
)
from apps.core.utils import (
    get_current_seconds,
)

from libretranslatepy import LibreTranslateAPI

SLEEP_TIME = 1  # seconds


class Common:
    def sleep(self, multiplier: int = 1) -> None:
        time.sleep(SLEEP_TIME * multiplier)
        return None


class WordnikApiProvider(Common):
    def __init__(self):
        self._base_url = "http://api.wordnik.com/v4"
        self._api_rate_limit_per_hour = 100  # per hour
        self._api_rate_limit = (60 * 60) / self._api_rate_limit_per_hour
        self._api_keys = WORDNIK_API_KEYS
        self._word_api_usage = dict()
        self._word_apis = dict()

        for api_key in self._api_keys:
            self._word_api_usage[api_key] = 0
            self._word_apis[api_key] = WordApi.WordApi(swagger.ApiClient(api_key, self._base_url))

    def next_word_api(self) -> WordApi.WordApi:
        while True:
            current = get_current_seconds()
            for api_key in self._api_keys:
                diff = current - self._word_api_usage[api_key]
                logger.debug(f"Finding Next WordApi: {api_key} > {diff} >= {self._api_rate_limit}")

                if current - self._word_api_usage[api_key] >= self._api_rate_limit:
                    self._word_api_usage[api_key] = current
                    logger.debug(f"Found Next WordApi: {api_key}")
                    return self._word_apis[api_key]

                self.sleep()


class WordnikService(metaclass=SingletonMeta):
    def __init__(self):
        self._api_keys = WORDNIK_API_KEYS
        self._base_url = "http://api.wordnik.com/v4"
        self._api_client = ApiClient()

        self.api_key_length = len(self._api_keys)
        self.api_key_queue = CircularQueue(self.api_key_length)
        self.word_apis = [None] * self.api_key_length

        self._api_provider = WordnikApiProvider()

        self.error_code_unauthorized = 401
        self.error_code_rate_limit = 429
        self.error_code_not_found = 404
        self.error_code_server = 500

        for index in range(self.api_key_length):
            self.api_key_queue.enqueue(index)
            client = swagger.ApiClient(self._api_keys[index], self._base_url)
            word_api = WordApi.WordApi(client)
            self.word_apis[index] = word_api

        # random iterate
        for index in range(random.randint(0, self.api_key_length)):
            self.api_key_queue.iterate()

    def sleep(self, multiplier: int = 1) -> None:
        time.sleep(SLEEP_TIME * multiplier)
        return None

    @property
    def _api_key(self) -> str:
        return self._api_keys[self.api_key_queue.peek()]

    @property
    def _word_api(self) -> WordApi.WordApi:
        return self.word_apis[self.api_key_queue.peek()]
        # return self._api_provider.next_word_api()

    def get_pronunciations(self, word, limit):
        main_limit = limit
        is_error = True
        result = None
        index = 0

        while index < self.api_key_length and limit > 0:
            try:
                result = self._word_api.getTextPronunciations(word, limit=limit)
                is_error = False
                break
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    if main_limit == limit:
                        index = index + 1
                    self.sleep(index + 1)
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
                elif error.code == self.error_code_server:
                    self.api_key_queue.iterate()
                    limit = limit - 1
                    self.sleep()
                    continue

        self.api_key_queue.iterate()
        self.sleep()

        return is_error, result

    def get_audios(self, word, limit):
        main_limit = limit
        is_error = True
        result = None
        index = 0

        while index < self.api_key_length and limit > 0:
            try:
                result = self._word_api.getAudio(word, limit=limit)
                is_error = False
                break
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    if main_limit == limit:
                        index = index + 1
                    self.sleep(index + 1)
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
                elif error.code == self.error_code_server:
                    self.api_key_queue.iterate()
                    limit = limit - 1
                    self.sleep()
                    continue

        self.api_key_queue.iterate()
        self.sleep()

        return is_error, result

    def get_definitions(self, word, limit):
        main_limit = limit
        is_error = True
        result = None
        index = 0

        while index < self.api_key_length and limit > 0:
            try:
                result = self._word_api.getDefinitions(word, limit=limit)
                is_error = False
                break
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    if main_limit == limit:
                        index = index + 1
                    self.sleep(index + 1)
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
                elif error.code == self.error_code_server:
                    self.api_key_queue.iterate()
                    limit = limit - 1
                    self.sleep()
                    continue

        self.api_key_queue.iterate()
        self.sleep()

        return is_error, result

    def get_examples(self, word, limit):
        main_limit = limit
        is_error = True
        result = None
        index = 0

        while index < self.api_key_length and limit > 0:
            try:
                result = self._word_api.getExamples(word, limit=limit)
                is_error = False
                break
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    if main_limit == limit:
                        index = index + 1
                    self.sleep(index + 1)
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
                elif error.code == self.error_code_server:
                    self.api_key_queue.iterate()
                    limit = limit - 1
                    self.sleep()
                    continue

        self.api_key_queue.iterate()
        self.sleep()

        return is_error, result

    def get_examples_rest(self, word, limit):
        main_limit = limit
        is_error = True
        result = None
        index = 0

        while index < self.api_key_length and limit > 0:
            try:
                url = f"{self._base_url}/word.json/{word}/examples"
                params = {
                    "limit": limit,
                    "api_key": self._api_key,
                }
                result = self._api_client.get(url=url, params=params)
                is_error = False
                break
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    if main_limit == limit:
                        index = index + 1
                    self.sleep(index + 1)
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
                elif error.code == self.error_code_server:
                    self.api_key_queue.iterate()
                    limit = limit - 1
                    self.sleep()
                    continue

        self.api_key_queue.iterate()
        self.sleep()

        return is_error, result

    def get_relations(self, word, limit):
        main_limit = limit
        is_error = True
        result = None
        index = 0

        while index < self.api_key_length and limit > 0:
            try:
                result = self._word_api.getRelatedWords(word, limitPerRelationshipType=limit)
                is_error = False
                break
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    if main_limit == limit:
                        index = index + 1
                    self.sleep(index + 1)
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
                elif error.code == self.error_code_server:
                    self.api_key_queue.iterate()
                    limit = limit - 1
                    self.sleep()
                    continue

        self.api_key_queue.iterate()
        self.sleep()

        return is_error, result


class Translator:
    limit = 3
    error_code_timeout = 504

    translator = LibreTranslateAPI("https://translate.argosopentech.com/")

    def sleep(self) -> None:
        time.sleep(SLEEP_TIME * 2)
        return None

    def languages(self):
        is_error = True
        result = None

        for index in range(self.limit):
            try:
                result = self.translator.languages()
                is_error = False
                break
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_timeout:
                    self.sleep()
                    continue

        return is_error, result

    def translate(self, text, source, target):
        is_error = True
        result = None

        for index in range(self.limit):
            try:
                result = self.translator.translate(text, source, target)
                is_error = False
                break
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_timeout:
                    self.sleep()
                    continue

        return is_error, result
