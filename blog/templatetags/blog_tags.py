from django import template

from ..models import Post

register = template.Library()


@register.simple_tag
def total_post():
    return Post.published.count()
