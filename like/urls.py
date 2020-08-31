from django.urls import path
from . import views


urlpatterns = [
    path('increase_likes', views.increase_likes, name='increase_likes')
]
