from django.test import TestCase

from libretranslatepy import LibreTranslateAPI


# Create your tests here.


class LibreTranslateApiTestCase(TestCase):
    def test_languages(self):
        translator = LibreTranslateAPI("https://translate.argosopentech.com/")
        for language in translator.languages():
            self.assertTrue(len(language["code"]) > 0)
            self.assertTrue(len(language["name"]) > 0)
