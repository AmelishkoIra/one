"""логика работы приложения"""
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, \
    SearchRank
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    """Обработчик отображения списка статей"""
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})

def post_detail(request, year, month, day, post):
    """Обработчик отображение деталей к статье"""
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    # Список активных комментариев для этой статьи.
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Пользователь отправил комментарийю
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье.
            new_comment.post = post
            # Сохраняем комментарий в базе данных.
            new_comment.save()
    else:
        comment_form = CommentForm()
    # Формирование списка похожих статей.
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).\
        exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).\
                        order_by('-same_tags', '-publish')[:4]


    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                  'comments': comments,
                  'new_comment': new_comment,
                  'comment_form': comment_form,
                  'similar_posts': similar_posts})

def post_share(request, post_id):
    """обработчик отправки письма с рекомендацией статьи"""
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],
                                                                   cd['email'],
                                                                   post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.\
                format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

def post_search(request):
    """обработчик поиска статей"""
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.object.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)
    return render(request, 'blog/post/search.html', {'form': form,
                                                    'query': query,
                                                    'results': results})


def other_page(request, page):
    try:
        template = get_template('blog/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

def alph_title(request):
    """Формирование списка статей по алфавиту"""
    alphabetical_title = Post.published.order_by('book_title')
    return render(request, 'blog/post/alph.html',
                  {'alphabetical_title': alphabetical_title})

def alph_author(request):
    """Формирование списка авторов по алфавиту"""
    alphabetical_author = Post.published.order_by('book_author')
    return render(request, 'blog/post/althauthor.html',
                  {'alphabetical_author': alphabetical_author})

def rating(request):
    """Формирование списка статей по рейтингу"""
    top_books = Post.published.filter(book_rating=10)
    return render(request, 'blog/post/rating.html', {'top_books': top_books})

# Create your views here.
