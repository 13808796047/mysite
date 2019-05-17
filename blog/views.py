from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from read_statistics.utils import read_statistics_once
from .models import Article, Category


def get_articles(request, articles):
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

    article_dates = Article.objects.dates('created_time', 'day', order='DESC')
    article_dates_dic = {}
    for article_date in article_dates:
        article_count = Article.objects.filter(created_time__year=article_date.year,
                                               created_time__month=article_date.month,
                                               created_time__day=article_date.day).count()
        article_dates_dic[article_date] = article_count

    categories = Category.objects.all()

    context = {
        'articles': page_of_articles,
        'page_range': page_range,
        'categories': categories,
        'article_dates': article_dates_dic,
    }
    return context


def article_list(request):
    articles = Article.objects.all()  # 全部文章
    context = get_articles(request, articles)
    return render_to_response('blog/article_list.html', context)


def articles_with_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    articles = Article.objects.filter(category=category)
    context = get_articles(request, articles)
    context['category'] = category

    return render_to_response('blog/articles_with_category.html', context)


def articles_with_date(request, year, month, day):
    articles = Article.objects.filter(created_time__year=year, created_time__month=month, created_time__day=day)
    context = get_articles(request, articles)
    articles_with_date = '%s年%s月%s日' % (year, month, day)
    context['articles_with_date'] = articles_with_date

    return render_to_response('blog/articles_with_date.html', context)


def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    read_cookie_key = read_statistics_once(request,article)
    previous_article = Article.objects.filter(created_time__gt=article.created_time).last()
    next_article = Article.objects.filter(created_time__lt=article.created_time).first()
    context = {
        'article': article,
        'previous_article': previous_article,
        'next_article': next_article
    }
    response = render_to_response('blog/article_detail.html', context)  # 设置阅读cookie
    response.set_cookie(read_cookie_key, 'true', max_age=60)
    return response
