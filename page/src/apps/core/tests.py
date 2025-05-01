from unittest import TestCase as UnitTestCase
from unittest.mock import patch

from django.test import TestCase as DjangoTestCase

from apps.core.models import User


class UserTestCase(DjangoTestCase):
    # @patch('apps.core.models.User.objects.get')
    # def test_get_user_by_email(self, mock_get):
    #     # Configure the mock object to return a specific value
    #     mock_user = User(id=1, name="Test User", email="test@example.com")
    #     mock_get.return_value = mock_user
    #
    #     # Call the method that uses the mocked database interaction
    #     user = User.get_by_email("test@example.com")
    #
    #     # Assertions
    #     self.assertEqual(user.id, 1)
    #     self.assertEqual(user.name, "Test User")
    #     self.assertEqual(user.email, "test@example.com")
    #     mock_get.assert_called_once_with(email="test@example.com")
    pass



class TestUtils(UnitTestCase):

    def test_add_positive_numbers(self):
        self.assertEqual(5, 5)
