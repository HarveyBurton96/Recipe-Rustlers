from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("add_a_recipe", views.add_recipe, name="add_recipe"),
]
