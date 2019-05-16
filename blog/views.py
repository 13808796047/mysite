from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Article, Category


def article_list(request):
    articles = Article.objects.all()  # 全部文章
    paginator = Paginator(articles, settings.PAGE_NUMBER)  # 每页10条进行分页
    page_num = request.GET.get('page', 1)  # 获取页面参数（GET请求）
    page_of_articles = paginator.get_page(page_num)  # 分页后的数据
    # 生成页码范围
    # 获取当前页码前后各两页
    page_range = [x for x in range(int(page_num) - 2, int(page_num) + 3) if 0 < x <= paginator.num_pages]
    # 加上首页和尾页
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    categories = Category.objects.all()
    context = {
        'articles': page_of_articles,
        'page_range': page_range,
        'categories': categories
    }
    return render_to_response('blog/article_list.html', context)


def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'article': article
    }
    return render_to_response('blog/article_detail.html', context)


def articles_with_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    articles = Article.objects.filter(category=category)

    paginator = Paginator(articles, settings.PAGE_NUMBER)  # 每页10条进行分页
    page_num = request.GET.get('page', 1)  # 获取页面参数（GET请求）
    page_of_articles = paginator.get_page(page_num)  # 分页后的数据
    # 生成页码范围
    # 获取当前页码前后各两页
    page_range = [x for x in range(int(page_num) - 2, int(page_num) + 3) if 0 < x <= paginator.num_pages]
    # 加上首页和尾页
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    categories = Category.objects.all()
    context = {
        'page_range': page_range,
        'articles': page_of_articles,
        'category': category,
        'categories': categories
    }
    return render_to_response('blog/articles_with_category.html', context)
