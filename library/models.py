from django.db import models
class User (models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    book_lists = models.ForeignKey(BookList, on_delete=models.CASCADE)

class User.admin (models.Model):
    pass

class Book (models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    isbn = models.IntegerField(max_length=13)
    published_year = models.IntegerField()
    categories = models.ManyToManyField(Category)
    pages = models.IntegerField() 
    material_url - models.URLField()
    available = models.BooleanField() 



class Category (models.Model):
    category_name = models.CharField(max_length=100, unique= True )

class BookCategory(models.Model):
    pass

class Review (models.Model):
    review_id = models.IntegerField(unique=True)
    book_reviewed = models.ForeignKey(Book, on_delete=models.CASCADE)
    star_rating = models.IntegerChoices({1,2,3,4,5})
    comment = models.TextField(max_length=300)
    upvotes = models.IntegerField(default=0) 
    date_of_review = models.DateField

class BookList (models.Model):
    list_name = models.CharField(max_length= 100)
    list_id = models.IntegerField(unique=True)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)




