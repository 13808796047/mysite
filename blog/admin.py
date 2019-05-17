from django.contrib import admin
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'category', 'author','get_read_num', 'created_time', 'updated_time')

'''
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num','article')
'''