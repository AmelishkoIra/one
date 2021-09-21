from django.urls import path, include
from . import views
from .feeds import LatestPostsFeed
from .views import other_page
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('<str:page>/', other_page, name='other'),
    path('alph', views.alph_title, name='post_alph'),
    path('alphauthor', views.alph_author, name='alph_author'),
    path('rating', views.rating, name='rating'),

]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)