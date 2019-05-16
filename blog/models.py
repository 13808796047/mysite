from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    def article_count(self):
        return self.article_set.count()


class Article(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Article:%s>" % self.title



    class Meta:
        ordering = ['-created_time']
