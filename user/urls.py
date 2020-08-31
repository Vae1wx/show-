from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('register/', views.register, name='register'),
    path('send_verification_code/', views.send_verification_code,
         name='send_verification_code'),
    path('email/', views.email, name='email'),
    path('user_info/', views.user_info, name='user_info'),
    path('image_code/', views.image_code, name='image_code'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('change_password/', views.change_password, name='change_password'),
    path('avatar', views.avatar, name='avatar'),

]
