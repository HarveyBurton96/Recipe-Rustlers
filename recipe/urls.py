from . import views
from django.urls import path, include

app_name = "recipe" 

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path('<slug:slug>/', views.PostDetail.as_view(), name="recipe_detail"),
    path("popular_recipe", views.PopularRecipes.as_view(), name="popular_recipe"),
    path("add_a_recipe", views.add_recipe, name="add_recipe"),
]
