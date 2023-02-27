from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Post, Comment, Ingredient, Instruction

STATUS = [(1, 'Draft'), (2, 'Published')]
DISH = ((0, "Breakfast"), (1, "Lunch"), (2, "Snack"), (3, "Dinner"), (4, "Dessert"))


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_image', 'status', 'surving', 'dish', 'prep', 'cook')

        status = forms.ChoiceField(choices=STATUS)
        dish = forms.ChoiceField(choices=DISH)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control-long'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control-long'}),
            'status': forms.Select(attrs={'class': 'form-control-medium'}),
            'surving': forms.NumberInput(attrs={'class': 'form-control-short'}),
            'dish': forms.Select(attrs={'class': 'form-control-medium'}),
            'prep': forms.NumberInput(attrs={'class': 'form-control-short'}),
            'cook': forms.NumberInput(attrs={'class': 'form-control-short'}),
        }

        labels = {
            'prep': 'Prep (minutes)',
            'cook': 'Cook (minutes)',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('ingredientName', 'weight', 'unit',)

        widgets = {
            'ingredientName': forms.TextInput(attrs={'class': 'form-control-long'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control-sm'}),
            'unit': forms.TextInput(attrs={'class': 'form-control-short'}),
        }

        labels = {
            'ingredientName': 'Ingredient name',
            'unit': 'Unit (if no unit then please enter -)',
        }


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ('step', 'detail',)

        widgets = {
            'step': forms.NumberInput(attrs={'class': 'form-control-short'}),
            'detail': forms.Textarea(attrs={'class': 'form-control-long'}),
        }

        labels = {
            'step': 'Please enter the step number',
            'detail': 'Please enter you steps instructions here',
        }
