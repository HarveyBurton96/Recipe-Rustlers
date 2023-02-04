from django.shortcuts import render
from django.views import generic, View
from .models import Post
from .forms import PostForm
from django.http import HttpResponseRedirect



class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('?')
    template_name = "index.html"
    paginate_by = 12


def add_recipe(request):
    submitted = False
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_a_recipe?submitted=True')
    else:
        form = PostForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'add_a_recipe.html', {'form': form, 'submitted': submitted})
