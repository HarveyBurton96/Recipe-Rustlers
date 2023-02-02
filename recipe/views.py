from django.shortcuts import render
from django.views import generic, View
from .models import Post
from .forms import PostForm




class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('?')
    template_name = "index.html"
    paginate_by = 12


def add_recipe(request):
    return render(request, 'add_a_recipe.html', {})
