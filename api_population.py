import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from library.models import Book, Category

SUBJECTS = {
    'Science':          'science',
    'Technology':       'technology',
    'History':          'history',
    'Arts':             'arts',
    'Medicine':         'medicine',
    'Fiction':          'fiction',
    'Computer Science': 'computer_science',
    'Comics':           'comics',
}


def fetch_books(subject, limit=15):
    url = 'https://openlibrary.org/search.json'
    params = {
        'subject': subject,
        'limit': limit,
        'fields': 'title,author_name,isbn,first_publish_year,number_of_pages_median,cover_i,key',
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('docs', [])
    except requests.RequestException as e:
        print(f"  Request failed: {e}")
    return []


def populate():
    print("Fetching books from Open Library API...\n")

    for category_name, subject_query in SUBJECTS.items():
        category, _ = Category.objects.get_or_create(category_name=category_name)
        print(f"Fetching: {category_name}")

        docs = fetch_books(subject_query)

        for doc in docs:
            isbn_list = doc.get('isbn', [])
            if not isbn_list:
                continue

            isbn = isbn_list[0][:13]
            title = doc.get('title', 'Unknown Title')
            authors = doc.get('author_name', ['Unknown Author'])
            author = authors[0] if authors else 'Unknown Author'
            published_year = doc.get('first_publish_year') or 2000
            pages = doc.get('number_of_pages_median') or 0
            cover_i = doc.get('cover_i')
            cover_url = f'https://covers.openlibrary.org/b/id/{cover_i}-M.jpg' if cover_i else ''
            ol_key = doc.get('key', '')
            material_url = f'https://openlibrary.org{ol_key}' if ol_key else ''

            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': title,
                    'author': author,
                    'published_year': published_year,
                    'pages': pages,
                    'cover_image_url': cover_url,
                    'material_url': material_url,
                    'available': True,
                }
            )
            book.categories.add(category)

            status = 'Created' if created else 'Exists'
            print(f"  [{status}] {title}")

    print(f"\nDone!")
    print(f"  {Book.objects.count()} books in database")
    print(f"  {Category.objects.count()} categories in database")


if __name__ == '__main__':
    populate()
