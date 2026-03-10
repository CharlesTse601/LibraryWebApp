from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [('student', 'Student'), ('admin', 'Admin')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_year = models.IntegerField()
    categories = models.ManyToManyField(Category)
    pages = models.IntegerField()
    material_url = models.URLField()
    available = models.BooleanField(default=True)
    cover_image_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class BookList(models.Model):
    LIST_TYPES = [('wishlist', 'Wishlist'), ('read', 'Read'), ('custom', 'Custom')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=100)
    list_type = models.CharField(max_length=10, choices=LIST_TYPES)
    books = models.ManyToManyField(Book, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star_rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=300)
    date_of_review = models.DateField(auto_now_add=True)

class Vote(models.Model):
    VOTE_CHOICES = [('like', 'Like'), ('dislike', 'Dislike')]
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)