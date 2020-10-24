from django.db import models
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User
from comments.models import Comment
from like.models import LikeCount
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.CharField(max_length=20)
    content = MDTextField()
    comment = GenericRelation(Comment)  # ContentType 反向查询
    likecount = GenericRelation(LikeCount)  # ContentType 反向查询
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    read_num = models.PositiveIntegerField(default=0)
    like_num = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


    def get_url(self):
        return self.pk

    class Meta:
        ordering = ['-created_time']
    