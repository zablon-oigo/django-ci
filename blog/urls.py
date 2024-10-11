from django.urls import path

from .views import post_detail, post_list, post_share

app_name = "blog"
urlpatterns = [
    path("<tag:tag_slug>/", post_list, name="list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", post_detail, name="detail"),
    path("<int:post_id>/share/", post_share, name="post_share"),
]
