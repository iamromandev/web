from urllib.error import HTTPError

from loguru import logger
from wordnik import swagger, WordApi

from apps.core.libs import CircularQueue


class WordnikService:
    def __init__(self):
        self.base_url = 'http://api.wordnik.com/v4'
        self.api_key_roman_bjit = '5c9a53f4c0e012d4cf5a66115420c073d7da523b9081dff1f'
        self.api_key_dreampany = '464b0c5a35f469103f3610840dc061f1c768aa1c223ffa447'
        self.api_key_iftenet = 'a6714f04f26b9f14e29a920702e0f03dde4b84e98f94fe6fe'

        self.api_keys = [self.api_key_roman_bjit, self.api_key_dreampany, self.api_key_iftenet]

        self.api_key_length = len(self.api_keys)
        self.api_key_queue = CircularQueue(self.api_key_length)
        self.word_apis = [None] * self.api_key_length
        self.error_code_rate_limit = 429
        self.error_code_not_found = 404

        for index in range(self.api_key_length):
            self.api_key_queue.enqueue(index)
            client = swagger.ApiClient(self.api_keys[index], self.base_url)
            word_api = WordApi.WordApi(client)
            self.word_apis[index] = word_api

    def get_word_api(self) -> WordApi.WordApi:
        return self.word_apis[self.api_key_queue.peek()]

    def get_pronunciations(self, word, limit):
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                pronunciations = word_api.getTextPronunciations(word, limit=limit)
                logger.debug(pronunciations)
                return pronunciations
            except HTTPError as error:
                logger.error(error)
                logger.exception('What?!')
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    break
        return None

    def get_audios(self, word, limit):
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                audios = word_api.getAudio(word, limit=limit)
                return audios
            except HTTPError as error:
                logger.exception('What?!')
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    break
        return None

    def get_definitions(self, word, limit):
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                definitions = word_api.getDefinitions(word, limit=limit)
                return definitions
            except HTTPError as error:
                logger.exception('What?!')
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    break
        return None

    def get_examples(self, word, limit):
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                examples = word_api.getExamples(word, limit=limit)
                return examples
            except HTTPError as error:
                logger.exception('What?!')
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    break
        return None

    def get_relations(self, word, limit):
        for index in range(self.api_key_length):
            try:
                word_api = self.get_word_api()
                relations = word_api.getRelatedWords(word, limitPerRelationshipType=limit)
                return relations
            except HTTPError as error:
                logger.exception('What?!')
                if error.code == self.error_code_rate_limit:
                    self.api_key_queue.iterate()
                    continue
                elif error.code == self.error_code_not_found:
                    break
        return None

