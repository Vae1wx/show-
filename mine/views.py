from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Blog
import markdown
from django.views.generic import ListView, TemplateView, DetailView
from django.core.paginator import Paginator  # 分页
# Create your views here.




class MineView(TemplateView):
    template_name = "mine.html"




class BlogListView(ListView):
    
    def get(self, request):
        blog = Blog.objects.all()
        page_cut = 4
        paginator = Paginator(blog, page_cut)  # 全部的博客列表，每x篇进行分页
        page_num = request.GET.get('page', 1)
        page_of_letter = paginator.get_page(page_num)
        current_page = page_of_letter.number  # 当前页

        page_range = list(range(max(current_page - 2, 1), current_page)) + list(
            range(current_page, min(current_page + 2, paginator.num_pages)+1))
        last_page = paginator.num_pages
        context = {}
        context['blogs'] = page_of_letter
        context["page_range"] = page_range
        context['last_page'] = last_page
        return render(request, 'blog_list.html', context)



class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog_detail.html"
    context_object_name = 'blog'

    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        blog.body = md.convert(blog.content)
        blog.toc = md.toc
        context = {}
        context['blog'] = blog  
        context['previous_blog'] = Blog.objects.filter(
        created_time__gt=blog.created_time).last()
        context['next_blog'] = Blog.objects.filter(
        created_time__lt=blog.created_time).first()
        return render(request, 'blog_detail.html', context)

# 留着参考 类视图
    # def get_object(self, blog_pk, querset=None):
    #     obj = super(BlogDetailView, self).get_object()
    #     blog = get_object_or_404(Blog, pk=blog_pk)
    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         'markdown.extensions.toc',
    #     ])
    #     obj.body = md.convert(obj.content)
    #     obj.toc = md.toc
    #     obj.previous_blog = Blog.objects.filter(title=123)
    #     obj.next_blog = Blog.objects.filter(created_time__lt=blog.created_time)
    #     return obj

   
