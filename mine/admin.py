from django.contrib import admin
from .models import Blog
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
	list_display = ['title', 'id', 'created_time', 'last_updated_time']
	search_fields = ['title']


admin.site.register(Blog, BlogAdmin)
