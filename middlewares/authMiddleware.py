from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse


class Authentication_Middleware(MiddlewareMixin):
    def process_request(self, request):
        # print(request.path_info) # 当前路由
        if request.path_info in settings.URL_WHITE_LIST:
            return
            
        if not request.user.is_authenticated and request.path_info != '/user/login/':
            return redirect('login')
            
      
