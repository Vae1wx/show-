from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from show.views import show_home

urlpatterns = [
    path('', show_home, name='home'),
    path('admin/', admin.site.urls),
    path('show/', include('show.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('mdeditor', include('mdeditor.urls')),
    path('user/', include('user.urls')),
    path('school/', include('school.urls')),
    path('comments/', include('comments.urls')),
    path('like/', include('like.urls')),
    path('accounts/', include('allauth.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
