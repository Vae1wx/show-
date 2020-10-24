from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import F
from .models import LikeCount
# Create your views here.


def dz(request, loveletter_pk):
   
    
    return HttpResponse(12)
