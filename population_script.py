import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from library.models import Book, Category, User

def populate():
    print("Populating database...")

    # Create categories
    categories_data = [
        'Science', 'Technology', 'History', 'Arts',
        'Medicine', 'Comics', 'Fiction', 'Computer Science'
    ]

    categories = {}
    for cat_name in categories_data:
        cat, created = Category.objects.get_or_create(category_name=cat_name)
        categories[cat_name] = cat
        print(f"  Category: {cat_name}")

    # Create books
    books_data = [
    {
        'isbn': '9780132350884',
        'title': 'Clean Code',
        'author': 'Robert C. Martin',
        'published_year': 2008,
        'pages': 464,
        'material_url': 'https://www.google.com',
        'available': True,
        'category': 'Computer Science',
    },
    {
        'isbn': '9780743273565',
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'published_year': 1925,
        'pages': 180,
        'material_url': 'https://www.google.com',
        'available': True,
        'category': 'Fiction',
    },
    {
        'isbn': '9780198321668',
        'title': 'A Brief History of Time',
        'author': 'Stephen Hawking',
        'published_year': 1988,
        'pages': 212,
        'material_url': 'https://www.google.com',
        'available': True,
        'category': 'Science',
    },
    ]
    for book_data in books_data:
        cat_name = book_data.pop('category')
        book, created = Book.objects.get_or_create(
            isbn=book_data['isbn'],
            defaults=book_data
        )
        book.categories.add(categories[cat_name])
        print(f"  Book: {book.title}")

    print("\nDone! Database populated.")
    print(f"  {Category.objects.count()} categories")
    print(f"  {Book.objects.count()} books")


if __name__ == '__main__':
    populate()
