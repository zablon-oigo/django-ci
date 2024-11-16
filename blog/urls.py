from django.urls import path

from .feeds import LatestPostsFeed
from .views import post_detail, post_list, post_search, post_share

app_name = "blog"
urlpatterns = [
    path("", post_list, name="list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", post_detail, name="detail"),
    path("<int:post_id>/share/", post_share, name="post_share"),
    path("feed/", LatestPostsFeed(), name="post-feed"),
    path("search/", post_search, name="post_search"),
    path("<slug:tag_slug>/", post_list, name="post_list_by_tag"),
]
