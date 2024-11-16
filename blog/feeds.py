from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy

from .models import Post


class LatestPostsFeed(Feed):
    title = "test post"
    link = reverse_lazy("blog:list")
    description = "New post test"

    def items(self):
        return Post.published.all()[:5]

    def items_title(self, item):
        return item.title

    def item_update(self, item):
        return item.publish
