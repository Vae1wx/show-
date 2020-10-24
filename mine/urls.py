from django.urls import path
from . import views

urlpatterns = [
    path('blog_list', views.BlogListView.as_view(), name='blog_list'),
    path('mine', views.MineView.as_view(), name='mine'),
    path('blog_detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),

]
