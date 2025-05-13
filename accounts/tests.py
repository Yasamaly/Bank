from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import User, Transaction

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(name="Alice", password="pass", money=1000)
        self.assertEqual(user.name, "Alice")

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(name="TestUser", password="testpass", money=1000)
        self.client.post(reverse('login'), {'name': 'TestUser', 'password': 'testpass'})  # Закрытые кавычки и скобки

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
