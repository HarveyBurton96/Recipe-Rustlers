from django.contrib import admin
from .models import Post, Comment, Ingredient, Instruction
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_filter = ('status', 'created_on')
    list_display = ('title', 'slug', 'status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('recipe', 'body', 'name', 'created_on')
    list_filter = ('created_on', 'name')
    search_fields = ['name', 'email', 'body']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredientName', 'unit')


@admin.register(Instruction)
class InstructionsAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'step', 'detail')
