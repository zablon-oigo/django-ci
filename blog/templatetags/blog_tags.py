from django import template

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("post/latest.html")
def show_latest_post(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


# @register.filter(name="markdown")
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))
