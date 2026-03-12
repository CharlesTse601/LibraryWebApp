from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import Book, Category, BookList, Review, Vote, User



def browse_view(request):
    # Get top 4 categories by number of books
    top_categories = Category.objects.annotate(
        book_count=Count('book')
    ).order_by('-book_count')[:4]

    # Get top 10 books by average star rating
    hot_books = Book.objects.annotate(
        avg_rating=Avg('review__star_rating')
    ).order_by('-avg_rating')[:10]

    return render(request, 'library/browse.html', {
        'top_categories': top_categories,
        'hot_books': hot_books,
    })



def search_view(request):
    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    category_filter = request.GET.get('category', '')

    # Start with all books, narrow down with filters
    books = Book.objects.all()

    # Search by title, author, or ISBN
    if query:
        books = books.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(isbn__icontains=query)
        )

    # Filter by date published
    if date_filter == '2020+':
        books = books.filter(published_year__gte=2020)
    elif date_filter == '2010-2019':
        books = books.filter(published_year__gte=2010, published_year__lte=2019)
    elif date_filter == 'before2010':
        books = books.filter(published_year__lt=2010)

    # Filter by category
    if category_filter:
        books = books.filter(categories__category_name=category_filter)

    # Add average rating to each book result
    books = books.annotate(avg_rating=Avg('review__star_rating'))

    all_categories = Category.objects.all()

    return render(request, 'library/search.html', {
        'books': books,
        'query': query,
        'result_count': books.count(),
        'all_categories': all_categories,
    })



def category_list_view(request):
    categories = Category.objects.annotate(
        book_count=Count('book')
    ).order_by('-book_count')

    # Featured = category with most books
    featured = categories.first()

    return render(request, 'library/categories.html', {
        'categories': categories,
        'featured': featured,
    })



def category_detail_view(request, category_name):
    category = get_object_or_404(Category, category_name=category_name)

    books = Book.objects.filter(
        categories=category
    ).annotate(avg_rating=Avg('review__star_rating'))

    return render(request, 'library/category_detail.html', {
        'category': category,
        'books': books,
    })




def book_detail_view(request, category_name, book_isbn):
    book = get_object_or_404(Book, isbn=book_isbn)
    reviews = Review.objects.filter(book=book).order_by('-date_of_review')
    avg_rating = reviews.aggregate(Avg('star_rating'))['star_rating__avg']

    return render(request, 'library/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })



@login_required
def add_review(request, book_isbn):
    book = get_object_or_404(Book, isbn=book_isbn)

    if request.method == 'POST':
        star_rating = request.POST.get('star_rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            book=book,
            user=request.user,
            star_rating=star_rating,
            comment=comment,
        )

    return redirect('book_detail', book_isbn=book_isbn)



@login_required
def vote_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    vote_type = request.POST.get('vote_type')  # 'like' or 'dislike'

    # Check if user already voted — update if so, create if not
    vote, created = Vote.objects.get_or_create(
        review=review,
        user=request.user,
        defaults={'vote_type': vote_type}
    )

    if not created:
        vote.vote_type = vote_type
        vote.save()

    return redirect(request.META.get('HTTP_REFERER', 'browse'))

@login_required
def profile_view(request):
    user = request.user
    lists = BookList.objects.filter(user=user)
    read_history = lists.filter(list_type='read').first()
    wishlist = lists.filter(list_type='wishlist').first()

    return render(request, 'library/profile.html', {
        'user': user,
        'lists': lists,
        'read_history': read_history,
        'wishlist': wishlist,
        'books_read': read_history.books.count() if read_history else 0,
        'review_count': Review.objects.filter(user=user).count(),
    })


@login_required
def add_to_list(request, list_id, book_isbn):
    book_list = get_object_or_404(BookList, id=list_id, user=request.user)
    book = get_object_or_404(Book, isbn=book_isbn)
    book_list.books.add(book)

    return redirect(request.META.get('HTTP_REFERER', 'browse'))

@login_required
def remove_from_list(request, list_id, book_isbn):
    book_list = get_object_or_404(BookList, id=list_id, user=request.user)
    book = get_object_or_404(Book, isbn=book_isbn)
    book_list.books.remove(book)

    return redirect(request.META.get('HTTP_REFERER', 'browse'))


@login_required
def mark_as_read(request, book_isbn):
    book = get_object_or_404(Book, isbn=book_isbn)

    # Get or create the user's read history list
    read_list, created = BookList.objects.get_or_create(
        user=request.user,
        list_type='read',
        defaults={'list_name': 'Read History'}
    )
    read_list.books.add(book)

    return redirect(request.META.get('HTTP_REFERER', 'browse'))

def recently_published_view(request):
    books = Book.objects.order_by('-published_year')[:20]
    return render(request, 'library/recently_published.html', {'books': books})

def about_us_view(request):
    return render(request, 'library/about_us.html')

def faq_view(request):
    return render(request, 'library/faq.html')

def contacts_view(request):
    return render(request, 'library/contacts.html')

def privacy_policy_view(request):
    return render(request, 'library/privacy_policy.html')

def terms_of_service_view(request):
    return render(request, 'library/terms_of_service.html')

def user_login_view(request):
    return render(request, 'library/login.html')

def user_logout_view(request):
    logout(request)
    return redirect('library:browse')

def my_books_view(request):
    lists = BookList.objects.filter(user=request.user)
    return render(request, 'library/my_books.html', {'lists': lists})