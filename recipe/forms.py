from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Post, Comment, Ingredient, Instruction
from django.template.defaultfilters import slugify

STATUS = [(1, 'Draft'), (2, 'Published')]
DISH = ((0, "Breakfast"), (1, "Lunch"), (2, "Snack"), (3, "Dinner"), (4, "Dessert"))


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'featured_image', 'author', 'status', 'surving', 'dish', 'prep', 'cook')

        status = forms.ChoiceField(choices=STATUS)
        dish = forms.ChoiceField(choices=DISH)
        author = User
        slug = slugify('title')

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


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('ingredientName', 'weight', 'unit',)


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ('step', 'detail',)
