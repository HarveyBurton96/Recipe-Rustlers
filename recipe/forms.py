from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Post, Comment

CHOICES = [(1, 'Draft'), (2, 'Published')]


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'featured_image', 'author', 'status', 'surving',)

        status = forms.ChoiceField(choices=CHOICES)
        author = User

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'surving': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
