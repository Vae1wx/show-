from ckeditor_uploader.fields import RichTextUploadingField # 富文本编辑器。
from django.contrib.auth.models import User
from django.db import models
from comments.models import Comment
from like.models import LikeCount
from mdeditor.fields import MDTextField
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.


class LoveLetter(models.Model):
    title = models.CharField( max_length=50)
    school = models.CharField(max_length=50)
    like_name = models.CharField(max_length=20)
    # content = RichTextUploadingField()  富文本编辑器
    content = MDTextField() # Markdown编辑器
    comment = GenericRelation(Comment)  # ContentType 反向查询
    likecount = GenericRelation(LikeCount)  # ContentType 反向查询
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    read_num = models.PositiveIntegerField(default=0)
    like_num = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']

    def get_user(self):
        return self.writer


    def get_url(self):
	    return self.pk
