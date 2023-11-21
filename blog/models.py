from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from mdeditor.fields import MDTextField
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT='DF','Draft'
        PUBLISHED='PB','Published'

    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250, unique_for_date="publish")
    content=MDTextField()
    image=models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects=models.Manager()
    published=PublishedManager()
    tags=TaggableManager()
    class Meta:
        ordering=['-publish']
        indexes=[
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return f'{self.title}'
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        self.slug=slugify(self.title)
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year,self.publish.month, self.publish.day,self.slug])
    

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=MDTextField()
    created=models.DateTimeField(auto_now_add=True)
    parent=models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=['created']
        indexes=[
            models.Index(fields=['created'])
        ]
    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'
    


