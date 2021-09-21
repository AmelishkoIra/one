"""регистрация модели для администрирования"""
from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Поля отображения сайта администрирования.

    Args:
    list_display -- отображение модели поста.
    list_filter -- фильтрация статей по полям.
    search_fields -- строка поиска.
    prepopulated_fields --
    raw_id_fields -- автоматическая генерация слаг.
    date_hierarchy -- навигация по датам.
    ordering -- сортировка статей по статусу и дате публикации.
    """
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Поля отображения администрирования комментариев к статье """
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

# Register your models here.
