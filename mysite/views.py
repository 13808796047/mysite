from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data
from blog.models import Article

def home(request):
    article_content_type = ContentType.objects.get_for_model(Article)
    dates,read_nums = get_seven_days_read_data(article_content_type)
    context = {
        'read_nums':read_nums,
        'dates':dates
    }
    return render_to_response('home.html', context)
