from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify
from django.urls import reverse

STATUS = ((0, "Draft"), (1, "Published"))
DISH = ((0, "Breakfast"), (1, "Lunch"), (2, "Snack"), (3, "Dinner"), (4, "Dessert"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, null=False, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe_posts")
    updated_on = models.DateTimeField(auto_now=True)
    featured_image = CloudinaryField('image', default='no_image')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    surving = models.IntegerField(default=2)
    likes = models.ManyToManyField(User, related_name='recipe_likes', blank=True)
    dish = models.IntegerField(choices=DISH, default=3)
    prep = models.IntegerField(default=0)
    cook = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    recipe = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class Ingredient(models.Model):
    recipe = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ingredients')
    ingredientName = models.CharField(max_length=80)
    weight = models.IntegerField(default=1)
    unit = models.CharField(max_length=80)


class Instruction(models.Model):
    recipe = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='instructions')
    step = models.IntegerField(1)
    detail = models.CharField(max_length=800)
