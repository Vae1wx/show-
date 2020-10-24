from django.http import HttpResponseRedirect
import random
import string
import time

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse

from user.forms import EmailForm, ForgetPassword, LoginForm, RegForm, ChangeNicknameForm, ChangePassword, ProfileForm
from .models import Profile


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        value = request.POST.get("code").upper()
        value2 = request.session.get("verCode", '').upper()
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None and value == value2:
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))
            elif value != value2:
                login_form.add_error(None, '验证码不正确')
            else:
                login_form.add_error(None, '用户名或密码不正确')
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)



def logout(request):
	auth.logout(request)
	return redirect(request.GET.get('from', reverse('home')))

def forget_password(request):
    if request.method == 'POST':
        form = ForgetPassword(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            del request.session['verification_code']
            return redirect(reverse('home'))
    else:
        form = ForgetPassword()
    context = {}
    context['form'] = form
    context['page_title'] = '忘记密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['return_back_url'] = reverse('home')
    return render(request, 'form.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 清除session
            del request.session['verification_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

def send_verification_code(request):
    email = request.GET.get('email', '')
    data = {}
    if email != '':
        code = ''.join(random.sample(string.ascii_letters +
                                     string.digits, 4))  # 生成的四个随机字母，变成列表形式。
        now_time = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now_time - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session['verification_code'] = code
            request.session['send_code_time'] = now_time
            send_mail('薛定谔的验证码', code, 
                      settings.EMAIL_HOST_USER,
                      [email],
                      fail_silently=False)
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    
    return JsonResponse(data)


def image_code(request):
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    img = Image.new(mode='RGB', size=(150, 30), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')
    font = ImageFont.truetype('collected_static\kumo.ttf', size=30)
    code = ''.join(random.sample(string.ascii_letters +
                                 string.digits, 4)) 
    request.session["verCode"] = code
    request.session.set_expiry(0)
    def rndColor():
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))
    for i in range(40):
        draw.point([random.randint(0, 120), random.randint(0, 30)],
                   fill=rndColor())
    draw.text([20, 1], code,  font=font, fill=rndColor())
    h = random.randint(0, 4)
   
    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    return HttpResponse(data)

   

def email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request=request)
        if form.is_valid():
            email = request.cleaned_data['email']
            request.user.email = email
            request.save()
            del request.session['email_code']
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = EmailForm()

    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back_url'] = request.GET.get('from', reverse('home'))
    return render(request, 'form.html', context)

def user_info(request):
    import datetime
    now = datetime.datetime.now()
    user_bir_time = User.date_joined
    
    context = {}
    context['now'] = now
    return render(request, 'user_info.html', context)


def avatar(request):
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user_id=request.user)
    if request.method == 'POST':
        # 上传的文件保存在 request.FILES 中，通过参数传递给表单类
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid() and 'avatar' in request.FILES:
            profile.avatar = profile_form.cleaned_data["avatar"]
            profile.save()
            return redirect('user_info')
        else:
            return HttpResponse("上传失败，请检查网络并重试。")
    else:
        return HttpResponse("请使用GET或POST请求数据")

def change_nickname(request):
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(request.GET.get('from', reverse('home'))) # 这里的from也需要在前端定义
    else:
        form = ChangeNicknameForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back_url'] = request.GET.get('from', reverse('home'))
    return render(request, 'form.html', context)


def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST, user=request.user)
        if form.is_vaild():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ChangePassword()
    
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back_url'] = request.GET.get('from', reverse('home'))
    return render(request, 'form.html', context)
