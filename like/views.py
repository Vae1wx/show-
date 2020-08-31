from django.shortcuts import render, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import LikeCount
# Create your views here.


def increase_likes(request):
    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')
    content_type = ContentType.objects.get(model=content_type)

    like_count, created = LikeCount.objects.get_or_create(
        content_type=content_type, object_id=object_id)
    like_count.like_num += 1
    like_count.save()
    return JsonResponse(like_count.like_num)
