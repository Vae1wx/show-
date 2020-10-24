from mycelery.sms.tasks import send_sms
from datetime import datetime
from datetime import timedelta
from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # 分页
from .forms import WriteForm
from notifications.models import Notification
from .models import LoveLetter  
from .static.words import words
from django.db.models import Q, F
import markdown
# Create your views here.

def show_home(request):
    context = {}
    return render(request, 'home.html', context)


def letter_list(request):
    hot_letter_list = LoveLetter.objects.all().order_by('-read_num')
    letter_list = LoveLetter.objects.all() # 取出全部letter
        
    # 分页
    page_cut = 4
    paginator = Paginator(letter_list, page_cut)  # 全部的博客列表，每x篇进行分页
    page_num = request.GET.get('page', 1)
    page_of_letter = paginator.get_page(page_num)
    current_page = page_of_letter.number # 当前页

    page_range = list(range(max(current_page - 2, 1), current_page)) + list(
        range(current_page, min(current_page + 2, paginator.num_pages)+1))
    last_page = paginator.num_pages

    # 补齐页码
    if last_page > 4:
        if current_page < 2:
            page_range.extend([current_page + 3, current_page + 4])
        elif current_page == 2:
            page_range.append(current_page + 3)
        elif last_page - current_page == 0:
            page_range.insert(0, last_page - 3)
            page_range.insert(0, last_page - 4)
        elif last_page - current_page == 1:
            page_range.insert(0, last_page - 3)
    elif last_page == 4:
        if current_page < 2:
            page_range.append(current_page + 3)
        elif last_page - current_page == 0:
            page_range.insert(0, last_page - 3)

    context = {}
    context['letters'] = page_of_letter
    context['page_range'] = page_range
    context['last_page'] = last_page
    context['hot_loveletter'] = hot_letter_list[:3]
    return render(request, 'letter_list.html', context)


def letter_content(request, loveletter_pk):
    context = {}
    loveletter = get_object_or_404(LoveLetter, pk=loveletter_pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    loveletter.body = md.convert(loveletter.content)

    if not request.COOKIES.get('loveletter_%s_readed' % loveletter_pk):
        loveletter.read_num += 1
        loveletter.save()
    # update_fields=[]指定了数据库只更新total_views字段，优化执行效率。
    loveletter.save(update_fields=['read_num'])
    context['loveletter'] = loveletter
    # context['toc'] = md.toc   不需要这个功能了
    context['previous_letter'] = LoveLetter.objects.filter(
        created_time__gt=loveletter.created_time).last()
    context['next_letter'] = LoveLetter.objects.filter(
        created_time__lt=loveletter.created_time).first()
    response = render(request, 'loveletter.html', context)
    # 点赞数
    if request.COOKIES.get('like_num') == 'true':
        loveletter.like_num -= 1
        
    elif request.COOKIES.get('like_num') == 'false':
        loveletter.like_num += 1
    loveletter.save()
    loveletter.save(update_fields=['like_num'])
    response.set_cookie('loveletter_%s_readed' %
                        loveletter_pk, 'true', max_age=60*60*24)
    return response

# write
def show_love(request):
    if request.method == 'POST':
        form = WriteForm(request.POST, user=request.user)
        if form.is_valid():
            title = request.POST.get('title')
            content = form.cleaned_data['content']
            school = request.POST.get('school')
            like_name = request.POST.get('like_name')
            content = request.POST.get('content')
            writer = User.username
            # 敏感词检测
            clean_word = words
            global new_word
            new_word = ''
            for i in content:
                if i in clean_word:
                    i = '*'
                new_word += i
            loveletter = LoveLetter.objects.create(title=title,
                                                   school=school, like_name=like_name, content=new_word, writer_id=request.session.get('_auth_user_id'))

            loveletter.save()
            return redirect(request.GET.get('from', reverse('home')))
        elif request.POST.get('content') == '':
            return render(request, 'error.html', {'message': '你啥都不写？'})
        elif User.is_authenticated:
            return render(request, 'error.html', {'message': '你还未登录'})

    context = {}
    context['WriteForm'] = WriteForm
    return render(request, 'write.html', context)


def revise_letter(request, loveletter_pk):
    loveletter = LoveLetter.objects.get(pk=loveletter_pk)
    # 接收到的前端数据
    data = {'title': loveletter.title,
            'school': loveletter.school,
            'like_name': loveletter.like_name,
            'content': loveletter.content}
    # 传入修改文章的表单
    form = WriteForm(data, request.POST, user=request.user)
    # 提交新的内容
    print(request.POST.get('title'))
    if request.method == "POST":
        loveletter.title = request.POST.get('title')
        loveletter.school = request.POST.get('school')
        loveletter.like_name = request.POST.get('like_name')
        loveletter.content = request.POST.get('content')
        # loveletter.title = title 正确做法会报错，暂时先不管了。
        loveletter.save()
    
        
    context = {'form': form}
    return render(request, 'revise_letter.html', context)
def sent(request):
    user_id = request.session.get('_auth_user_id') # 获取当前登录用户的id
    sent_list = LoveLetter.objects.filter(writer=user_id)
    context = {}
    context['sent_list'] = sent_list
    return render(request, 'sent.html', context)


def delete_letter(request, loveletter_pk):
    user_id = request.session.get('_auth_user_id')
    delete_letter = LoveLetter.objects.filter(
        writer=user_id, pk=loveletter_pk).delete()
    
    return redirect("sent")


# 站内搜索
def search_for(request):
    keyword = request.GET.get('word', '').strip()
    for word in keyword.split(' '):
        condition = Q(title__icontains=keyword) # 条件为空，加条件

    returned = LoveLetter.objects.filter(condition)
    
    page_cut = 4
    paginator = Paginator(returned, page_cut)  # 全部的博客列表，每x篇进行分页
    page_num = request.GET.get('page', 1)
    page_of_letter = paginator.get_page(page_num)
    current_page = page_of_letter.number  # 当前页

    page_range = list(range(max(current_page - 2, 1), current_page)) + list(
        range(current_page, min(current_page + 2, paginator.num_pages)+1))
    last_page = paginator.num_pages

    context = {}
    context['keyword'] = keyword
    context['returned'] = page_of_letter
    context['page_range'] = page_range
    context['last_page'] = last_page
    return render(request, 'search_for.html', context)


def my_notifications(request):
    return render(request, 'my_notifications.html')

def mark_readed(request):
    Notification.objects.all().mark_all_as_read()
    return redirect('my_notifications')


def delete_my_notifications(request):
    request.user.notifications.read().delete()
    return redirect('my_notifications')


def my_notification(request, my_notification_pk):
    my_notification = get_object_or_404(Notification, pk=my_notification_pk)
    my_notification.unread = False
    my_notification.save()
    print(my_notification.data['url'])
    return redirect(my_notification.data['url'])

def test(request):

    ################################# 异步任务

    # 1. 声明一个和celery一模一样的任务函数，但是我们可以导包来解决

    # send_sms.delay("110")
    
    # send_sms.delay() #如果调用的任务函数没有参数，则不需要填写任何内容

    ################################# 定时任务

    ctime = datetime.now()
    # 默认用utc时间
    utc_ctime = datetime.utcfromtimestamp(ctime.timestamp())
    time_delay = timedelta(seconds=10)
    task_time = utc_ctime + time_delay
    result = send_sms.apply_async(["911", ], eta=task_time)
    print(result.id)

    return HttpResponse('ok')


def zzz(request, loveletter_pk):
    loveletter = get_object_or_404(LoveLetter, pk=loveletter_pk)
    if request.COOKIES.get('is_like'):
        loveletter.like_num += 1
        loveletter.save()
        print(123)
    return HttpResponse(123)
def message(request):
    return render(request, 'message.html')
