"""carpetofflowers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "blog"

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('news', views.NewsView.as_view(), name='news'),
    path('boardgames', views.BoardgamesViews.as_view(), name='boardgames'),
    path('videogames', views.VideogamesViews.as_view(), name='videogames'),
    path('search', views.search_results, name='search'),
    path('register', views.register, name='register'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<slug>', views.article),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
