from django.contrib import admin
from .models import LoveLetter
# Register your models here.


class LoveLetterAdmin(admin.ModelAdmin):
	list_display = ['school', 'like_name', 'content', 'writer',
                 'id', 'created_time', 'last_updated_time']
	search_fields = ['like_name']


admin.site.register(LoveLetter, LoveLetterAdmin)  # 把文章模型注册到admin模块
