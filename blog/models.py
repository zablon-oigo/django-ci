from django.db import models
from django.utils import timezone
from django.urls import reverse
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
class Post(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
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

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,self.publish.month,self.publish.day,self.slug])
