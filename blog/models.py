from datetime import datetime 
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField('', max_length=30)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField('Название', max_length=100)
    body = HTMLField('Текст статьи')
    slug = models.SlugField('Название в виде url', max_length=200)
    author = models.CharField('Автор', max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,  
        related_name='articles',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
        )
    image = models.ImageField('Картинка', default='lea-232-black-lotus.jpeg')

    def snippet(self):
        return self.body[:200] + '...'

    def featured_snippet(self):
        return self.body[:300] + '...'

    def __str__(self):
        return self.title

class Comment(models.Model):
    username = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField('Текст комментария')
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f'{self.article.title} - {self.username} says: {self.body[:20]}...'

