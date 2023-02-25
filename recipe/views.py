from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from .models import Post
from .forms import PostForm, CommentForm, IngredientForm, InstructionForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.text import slugify
from cloudinary.forms import cl_init_js_callbacks


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('?')
    template_name = "index.html"
    paginate_by = 12


def SearchRecipe(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)
        return render(
            request,
            "search_recipe.html",
            {
                'searched': searched,
                "posts": posts,
            })
    else:
        return render(
            request,
            "search_recipe.html",
            {})


class PopularRecipes(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).annotate(like_count=Count('likes')).order_by('-like_count')
    template_name = "popular_recipe.html"
    paginate_by = 12


class NewRecipes(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = "new_recipe.html"
    paginate_by = 12


class LovedRecipes(generic.ListView):
    model = Post
    template_name = "loved_recipes.html"
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        queryset = user.recipe_likes.all()
        return queryset


def add_recipe(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.slug = slugify(form.cleaned_data.get('title'))
            print(form.slug)
            form.save()
            return redirect('recipe:add_a_recipe_detail', slug=form.slug)
    else:
        form = PostForm()

    return render(
        request,
        'add_a_recipe.html',
        {
            'form': form,
        },
    )


class add_recipeDetails(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        ingredients = post.ingredients.order_by('ingredientName')
        instructions = post.instructions.order_by('step')

        return render(
            request,
            "add_a_recipe_detail.html",
            {
                "post": post,
                "ingredients": ingredients,
                "instructions": instructions,
                "instruction_form": InstructionForm(),
                "ingredient_form": IngredientForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        ingredients = post.ingredients.order_by('ingredientName')
        instructions = post.instructions.order_by('step')

        ingredient_form = IngredientForm(data=request.POST)

        if ingredient_form.is_valid():
            ingredient = ingredient_form.save(commit=False)
            ingredient.recipe = post
            ingredient.save()
        else:
            ingredient_form = IngredientForm()

        instruction_form = InstructionForm(data=request.POST)

        if instruction_form.is_valid():
            instruction = instruction_form.save(commit=False)
            instruction.recipe = post
            instruction.save()
        else:
            instruction_form = InstructionForm()

        return render(
            request,
            "add_a_recipe_detail.html",
            {
                "post": post,
                "ingredients": ingredients,
                "instructions": instructions,
                "instruction_form": InstructionForm(),
                "ingredient_form": IngredientForm(),
            },
        )


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('created_on')
        ingredients = post.ingredients.order_by('ingredientName')
        instructions = post.instructions.order_by('step')
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
        ingredients = post.ingredients.order_by('ingredientName')
        instructions = post.instructions.order_by('step')
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


class RecipeLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('recipe:recipe_detail', args=[slug]))
