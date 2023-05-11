import random

from urllib.error import HTTPError

from loguru import logger
from wordnik import swagger, WordApi

from config.settings import WORDNIK_API_KEYS
from apps.core.libs import CircularQueue

from libretranslatepy import LibreTranslateAPI


class WordnikService:
    def __init__(self):
        self.base_url = "http://api.wordnik.com/v4"
        self.api_keys = WORDNIK_API_KEYS

        self.api_key_length = len(self.api_keys)
        self.api_key_queue = CircularQueue(self.api_key_length)
        self.word_apis = [None] * self.api_key_length
        self.error_code_unauthorized = 401
        self.error_code_rate_limit = 429
        self.error_code_not_found = 404
        self.error_code_server = 500

        for index in range(self.api_key_length):
            self.api_key_queue.enqueue(index)
            client = swagger.ApiClient(self.api_keys[index], self.base_url)
            word_api = WordApi.WordApi(client)
            self.word_apis[index] = word_api

        # random iterate
        for index in range(random.randint(0, self.api_key_length)):
            self.api_key_queue.iterate()

    def get_word_api(self) -> WordApi.WordApi:
        return self.word_apis[self.api_key_queue.peek()]

    def get_pronunciations(self, word, limit):
        is_error = True
        result = None
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                result = word_api.getTextPronunciations(word, limit=limit)
                is_error = False
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
        return is_error, result

    def get_audios(self, word, limit):
        is_error = True
        result = None
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                result = word_api.getAudio(word, limit=limit)
                is_error = False
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
        return is_error, result

    def get_definitions(self, word, limit):
        is_error = True
        result = None
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                result = word_api.getDefinitions(word, limit=limit)
                is_error = False
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
        return is_error, result

    def get_examples(self, word, limit):
        is_error = True
        result = None
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                result = word_api.getExamples(word, limit=limit)
                is_error = False
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
        return is_error, result

    def get_relations(self, word, limit):
        is_error = True
        result = None
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                result = word_api.getRelatedWords(word, limitPerRelationshipType=limit)
                is_error = False
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    is_error = False
                    break
        return is_error, result


class TranslatorService:

    limit = 3
    error_code_timeout = 504

    translator = LibreTranslateAPI('https://translate.argosopentech.com/')

    def languages(self):
        is_error = True
        result = None
        for index in range(self.limit):
            try:
                result = self.translator.languages()
                is_error = False
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_timeout:
                    continue
        return is_error, result

    def translate(self, text, source, target):
        is_error = True
        result = None
        for index in range(self.limit):
            try:
                result = self.translator.translate(text, source, target)
                is_error = False
            except HTTPError as error:
                logger.error(error)
                if error.code == self.error_code_timeout:
                    continue
        return is_error, result
