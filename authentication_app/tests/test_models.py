# tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'birthdate': '2000-01-01',
        }

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])
        self.assertEqual(str(user.birthdate), self.user_data['birthdate'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(**self.user_data)

        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)
