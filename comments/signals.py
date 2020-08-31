from django.db.models.signals import post_save
from django.dispatch import receiver  # 接收器，是一个装饰器。
from django.utils.html import strip_tags  # 回复评论用的
from notifications.signals import notify
from .models import Comment

@receiver(post_save, sender=Comment)
def send_notification(sender, instance, *args, **kwargs):
    if instance.reply_to is None: # 不是回复 说明是评论
        recipient = instance.content_object.get_user()
        if instance.content_type.model == 'loveletter':
            loveletter = instance.content_object
            verb = '评论了你的《loveletter.title》'
                   
        else:
            raise Exception('出错了')
    else:
        recipient = instance.content_object.get_user()
        verb = '回复了你的《strip_tags(instance.parent.text)》'
    url = str(instance.content_object.get_url()) + '/#comment_' + str(instance.pk)  # content_object 评论实体
    
    notify.send(instance.user, recipient=recipient, verb=verb,  url=url)
