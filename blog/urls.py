from django.urls import path
from .views import post_list,post_detail
app_name='blog'
urlpatterns=[
    path("",post_list,name="list"),
    path("<int:id>/",post_detail,name="detail"),
]