from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import PostForm, CommentForm
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
                "commented": False,
                "ingredients": ingredients,
                "instructions": instructions,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('created_on')
        ingredients = post.ingredients
        instructions = post.instructions
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "recipe_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "ingredients": ingredients,
                "instructions": instructions,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )
