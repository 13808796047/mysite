from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpand, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation


class Category(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    def article_count(self):
        return self.article_set.count()


class Article(models.Model, ReadNumExpand):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Article:%s>" % self.title

    class Meta:
        ordering = ['-created_time']


'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    article = models.OneToOneField(Article, on_delete=models.DO_NOTHING)
'''
