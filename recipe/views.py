from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import PostForm
from django.http import HttpResponseRedirect


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('?')
    template_name = "index.html"
    paginate_by = 12


class PopularRecipes(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('likes')
    template_name = "popular_recipe.html"
    paginate_by = 12


class NewRecipes(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = "new_recipe.html"
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


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('created_on')
        ingredients = post.ingredients
        instructions = post.instructions
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "recipe_detail.html",
            {
                "post": post,
                "comments": comments,
                "ingredients": ingredients,
                "instructions": instructions,
                "liked": liked
            },
        )
