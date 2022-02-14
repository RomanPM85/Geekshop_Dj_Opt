from django.conf import settings
from django.test import TestCase

from authapp.models import User
from mainapp.models import ProductCategory, Product
from django.test.client import Client


# Create your tests here.

class UserTestCase(TestCase):
    """ Данные администратора """
    username = 'django'
    email = 'django@mail.ru'
    password = 'TestSUser_1'

    """ Данные пользователя """
    new_user_data = {
        'username': 'TestUser2',
        'first_name': 'TestUser2',
        'last_name': 'TestUser2',
        'email': 'TestUser1@mail.ru',
        'password1': 'TestUserPas_1',
        'password2': 'TestUserPas_1',
        'age': 36,
    }

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 302)

    def test_register(self):
        response = self.client.post('/users/register/', data=self.new_user_data)
        print(response.status_code)  # печатаем код статус для проверки
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username=self.new_user_data['username'])
        """ структура из urls: verify / < str: email > / < str: activate_key > /
        для создания ссылки активации пользователя """

        activation_url = f"{settings.DOMAIN_NAME}/users/verify/{user.email}/{user.activation_key}/"
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(user.is_active)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def tearDown(self) -> None:
        pass
