from django.contrib import admin

from .models import Article, Category, Comment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
        'author'
    ]
    inlines = [CommentInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(AuthUserAdmin):
    inlines = [CommentInline]

