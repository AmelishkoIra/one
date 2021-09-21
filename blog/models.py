"""модели данных приложения"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from .utilities import get_timestamp_path

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    """Модель данных для статей блога.

    Args:
    title -- поле заголовка статьи.
    slug -- поле для краткого названия статьи.
    author -- поле автора статьи.
    book_title -- поле полного названия книги.
    book_author -- поле автора книги.
    book_rating -- поле рейтинга книги.
    body -- поле основного содержания статьи.
    publish -- поле даты публикации статьи.
    created -- поле даты создания статьи.
    updated -- поле даты и времени, когда статья была отредактирована.
    status -- поле статуса статьи.
    object -- менеджер модели.
    tags -- поле тегов статей.
    image -- поле изображений статей.
        """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    book_title = models.CharField(max_length=400, null=True)
    book_author = models.CharField(max_length=250, null=True)
    book_rating = models.CharField(max_length=2, null=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')
    object = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    image = models.ImageField(blank=True, upload_to=get_timestamp_path,
                              verbose_name='Изображение')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comment(models.Model):
    """Модель данных коментариев к статье блога.

    Args:
    post -- статья, к которой оставлен комментарий.
    name -- поле имени комментатора.
    email -- поле электронной почты комментатора.
    body -- поле содержания коментария.
    created -- поле даты создания комментария.
    updated -- поле даты и времени, когда комментарий был отредактирован
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


