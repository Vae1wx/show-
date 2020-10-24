from django.urls import path
from . import views


urlpatterns = [
    path('dz',views.dz,name='dz'),
    path('<int:loveletter_pk>/dz/', views.dz, name='dz'),
]
