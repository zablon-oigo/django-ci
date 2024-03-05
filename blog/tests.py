from django.test import TestCase
from .models import Post
from django.urls import reverse
from django.contrib.auth import get_user_model

class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user=get_user_model().objects.create_user(
            username="testuser",
            password="secret",
            email="testuser@mail.com"
        )
        cls.post=Post.objects.creat(
            title="Demo title",
            slug="demo-title",
            author=cls.user,
            content="Demo text"
        )

