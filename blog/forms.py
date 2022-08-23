from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']