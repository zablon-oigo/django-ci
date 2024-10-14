import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

User = get_user_model()


class UsersMnagersTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@user.com", password="test")
        self.assertEqual(user.email, "test@user.com")
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
            User.objects.create_user(email="", password="test")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="superuser@mail.com", password="test"
        )
        self.assertEqual(admin_user.email, "superuser@mail.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="superuser@mail.com", password="test", is_superuser=False
            )


@pytest.mark.django_db
class TestCustomUserModel:
    @pytest.fixture
    def create_user(self):
        return User.objects.create_user(
            email="testuser@example.com", username="testuser", password="password123"
        )

    def test_user_creation(self, create_user):
        user = create_user
        assert user.email == "testuser@example.com"
        assert user.username == "testuser"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.date_joined <= timezone.now()

    def test_user_str(self, create_user):
        user = create_user
        assert str(user) == user.username

    def test_user_secret_key(self, create_user):
        user = create_user
        assert user.secret_key is None
        user.secret_key = "some_secret_key"
        user.save()
        assert user.secret_key == "some_secret_key"
