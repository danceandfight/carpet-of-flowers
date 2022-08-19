from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.db.models import fields
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django import forms
from .forms import CommentForm 
from .models import Article, Comment


class HomepageView(generic.ListView):
    template_name = '../templates/homepage.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.all().order_by('-date').prefetch_related('category')


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
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    context = {'form': form}

    return render(request, 'registration.html', context)

