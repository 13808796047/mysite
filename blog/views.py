from django.shortcuts import render_to_response, get_object_or_404
from .models import Article, Category


def article_list(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    context = {
        'articles': articles,
        'categories':categories
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
    context = {
        'articles': articles,
        'category':category,
    }
    return render_to_response('blog/articles_with_category.html', context)
