from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.db.models import Prefetch
from .forms import CommentForm 
from django import forms
from django.contrib.auth.models import User

# Create your views here.

from .models import Article, Comment

from django.contrib.auth.decorators import login_required

class HomepageView(generic.ListView):
    template_name = '../templates/homepage.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.all().order_by('-date').prefetch_related('category')


from django.db.models import fields
from django.forms import ModelForm

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

def article(request, slug):
    comments_and_users = Comment.objects.filter(article__slug=slug).select_related('username')
    query = Article.objects.prefetch_related(Prefetch('comments', queryset=comments_and_users))
    article = get_object_or_404(query, slug=slug)
    if request.method == 'POST': 
        form = CommentForm(data=request.POST) 
        if form.is_valid(): 
            new_comment=form.save(commit=False) 
            new_comment.article=article
            new_comment.username=request.user 
            new_comment.save() 
            csubmit=True 
            return redirect(f'/{slug}')
    else:
        form=CommentForm()
    return render(request, 'article.html', context={
        'article': article,
        'comments': article.comments.all(),
        'form': form,
        })

#widget=forms.Textarea(attrs={'cols': 10, 'rows': 20})

class NewsView(generic.ListView):
    template_name = '../templates/news.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(category__name__icontains='news').order_by('-date').prefetch_related('category')

class BoardgamesViews(generic.ListView):
    template_name = '../templates/boardgames.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(category__name__icontains='boardgames').order_by('-date').prefetch_related('category')

class VideogamesViews(generic.ListView):
    template_name = '../templates/videogames.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(category__name__icontains='videogames').order_by('-date').prefetch_related('category')


def search_results(request):
    query_dict = request.GET
    query = query_dict.get("q")
    articles = Article.objects.filter(body__contains=query).prefetch_related('category')
    return render(request, 'search_results.html', context={
        'articles': articles,
        'query': query,
        })


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    context = {'form' : form}

    return render(request, 'registration.html', context)

def register2(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    context = {'form' : form}

    return render(request, 'reg2.html', context)

"""
#def add_comment(request):
    if request.method=='POST': 
        form=CommentForm(data=request.POST) 
        if form.is_valid(): 
            new_comment=form.save(commit=False) 
            new_comment.post=post 
            new_comment.save() 
            csubmit=True 
    else:
        form=CommentForm()
    return render(request,'blog/detail.html',{'post':post,'comments':comments,'csubmit':csubmit,'form':form})
"""




#def homepage(request):
#    articles = Article.objects.all().order_by('-date').prefetch_related('category')
#    """dumped_articles = serialize_articles(articles)
#    return render(request, 'homepage.html', context={
#        'articles': dumped_articles[1:],
#        'featured': dumped_articles[0]
#        })"""
#    return render(request, 'homepage.html', context={
#        'articles': dumped_articles})
#    """return render(request, 'homepage.html', context={
#        'articles': articles[1:],
#        'featured': articles[0]})"""



"""

def serialize_articles(articles):
    dumped_articles = []
    for article in articles:
        dumped_article = {
            'id': article.id,
            'title': article.title,
            'body': article.body,
            'slug': article.slug,
            'author': article.author,
            'category': {
                'id': article.category.id,
                'name': article.category.name,
            },
            'snippet': article.snippet(),
            'featured_snippet' : article.featured_snippet(),
            'image': article.image
        }
        dumped_articles.append(dumped_article)
    return dumped_articles

def article_page(request, slug):
    article = get_object_or_404(Article, slug=slug)
    dumped_article = {
        'title': article.title,
        'body': article.body
    }
    return render(request, 'article.html', context={
        'article': dumped_article
        })
"""


"""class SearchresultView(generic.ListView):
    template_name = '../templates/search_results.html'
    context_object_name = 'articles', 'query'

    def get(self, request, *args, **kwargs):
        query_dict = request.GET
        query = query_dict.get("q")
        return query

    def get_queryset(self):
        query = get(self, request)
        return Article.objects.filter(body__contains=query).prefetch_related('category')
"""

"""
def news_page(request):
    articles = Article.objects.filter(category__name__contains='news').prefetch_related('category')
    dumped_articles = serialize_articles(articles)
    return render(request, 'news.html', context={
        'articles': dumped_articles,
        })

def boardgames_page(request):
    articles = Article.objects.filter(category__name__contains='boardgames').prefetch_related('category')
    dumped_articles = serialize_articles(articles)
    return render(request, 'boardgames.html', context={
        'articles': dumped_articles
        })

def videogames_page(request):
    articles = Article.objects.filter(category__name__contains='videogames').prefetch_related('category')
    dumped_articles = serialize_articles(articles)
    return render(request, 'videogames.html', context={
        'articles': dumped_articles
        })"""

"""
def category_page(request, category):
    category_name = category.name
    category_items = Article.objects.filter(category=category)
    return render(request, f'{category_name}.html', context={
        'category_items': articles
        })
"""

"""
def get_absolute_url(self):
    return reverse('post_detail', kwargs={'slug': self.slug})
views.py

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})
urls.py

#...

urlpatterns = [
    path('articles/<slug>/', views.post_detail, name='post_detail'),
]
HTML

<a href="{{ post.get_absolute_url }}"> ... </a>
"""




"""
    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })
"""