from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='昵称')
    nickname = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    def __str__(self):
        return self.nickname

    
def get_nickname(self):
	if Profile.objects.filter(user=self).exists():
		profile = Profile.objects.get(user=self)
		return profile.nickname
	else:
		return ''


User.get_nickname = get_nickname

def get_avatar(self):
    if Profile.objects.filter(user=self).exists():
	    profile = Profile.objects.get(user=self)
    return profile.avatar


User.get_avatar = get_avatar
