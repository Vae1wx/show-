from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.show_home, name='show_home'),
    path('show_love/', views.show_love, name='show_love'),
    path('letter_list/', views.letter_list, name='letter_list'),
    path('<int:loveletter_pk>/', views.letter_content, name='letter_content'),
    path('sent/', views.sent, name='sent'),
    path('delete_letter/<int:loveletter_pk>/',
         views.delete_letter, name='delete_letter'),
    path('search_for/', views.search_for, name='search_for'),
    path('my_notifications', views.my_notifications, name='my_notifications'),
    path('mark_readed/', views.mark_readed, name='mark_readed'),
    path('delete_my_notifications', views.delete_my_notifications,
         name='delete_my_notifications'),
    path('test/', views.test, name='test'),
    path('revise_letter/<int:loveletter_pk>/',
         views.revise_letter, name='revise_letter'),
    path('<int:my_notification_pk>',
         views.my_notification, name='my_notification'),
    path('message/', views.message, name='message'),
         
]
