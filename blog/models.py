from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT='DF','Draft'
        PUBLISHED='PB','Published'
    title=models.CharField(max_length=200)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='blog_posts')
    slug=models.SlugField(max_length=200,unique_for_date='publish')
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    objects=models.Manager()
    published=PublishedManager()
    class Meta:
        ordering=['-publish']
        indexes=[
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.publish.year,self.publish.month,self.publish.day,self.slug])
