from django.test import TestCase
from django.contrib.auth import get_user_model

class UsersMnagersTest(TestCase):
    def test_create_user(self):
        User=get_user_model()
        user=User.objects.create_user(
            email="test@user.com",
            password="test"
        )
        self.assertEqual(user.email,"test@user.com")
        self.assertEqual(user.is_staff)
        self.assertEqual(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="",password="test")
