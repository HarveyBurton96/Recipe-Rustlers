from . import views
from django.urls import path, include

app_name = "recipe"

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path('<slug:slug>/', views.PostDetail.as_view(), name="recipe_detail"),
    path('add_a_recipe_detail/<slug:slug>', views.add_recipeDetails.as_view(), name="add_a_recipe_detail"),
    path("popular_recipe", views.PopularRecipes.as_view(), name="popular_recipe"),
    path("new_recipe", views.NewRecipes.as_view(), name="new_recipe"),
    path("add_a_recipe", views.add_recipe, name="add_recipe"),
    path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
    path("loved_recipes",  views.LovedRecipes.as_view(), name="loved_recipes"),
    path("search_recipe",  views.SearchRecipe, name="search_recipe"),
    path('update_recipe/<slug:slug>', views.UpdateRecipe, name="update_recipe"),
    path("your_recipes",  views.YourRecipes.as_view(), name="your_recipes"),
    path('your_recipe/<slug:slug>/', views.YourPostDetail.as_view(), name="your_recipe_detail"),

]
