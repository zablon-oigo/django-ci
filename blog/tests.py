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
    def test_model_content(self):
        self.assertEqual(self.post.title, "Demo title")
        self.assertEqual(self.post.slug, "demo-title")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.content, "Demo text")
        self.assertEqual(str(self.post), "Demo title")

    
    def test_post_list_view(self):
        response=self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demo title")
        self.assertTemplateUsed(response, "post_list.html")
    
    def test_post_detail_view(self):
        response=self.client.get(reverse("post_detail", kwargs={"pk":self.post.pk, "slug":self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demo title")
        self.assertTemplateUsed(response, "post_detail.html")
   
    def test_post_create_view(self):
        response=self.client.post(reverse("create"),{
            "title":"updated title",
            "content":"new content"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "updated title")
        self.assertEqual(Post.objects.last().content, "new content")
