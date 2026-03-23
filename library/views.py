from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.contrib.auth import login , logout , authenticate, update_session_auth_hash
from django.db.models import Avg, Count,Q
from django.urls import reverse 
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
    user_lists = BookList.objects.filter(user=request.user) if request.user.is_authenticated else []

    return render(request, 'library/browse.html', {
        'top_categories': top_categories,
        'hot_books': hot_books,
        'user_lists':user_lists,
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
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
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




def book_detail_view(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    reviews = Review.objects.filter(book=book).order_by('-date_of_review')
    avg_rating = reviews.aggregate(Avg('star_rating'))['star_rating__avg']
    review_count = reviews.count()
    user_lists = BookList.objects.filter(user=request.user) if request.user.is_authenticated else []

    return render(request, 'library/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count':review_count, 
        'user_lists':user_lists ,
    })



@login_required
def add_review(request, book_isbn):
    book = get_object_or_404(Book, isbn=book_isbn)

    if request.method == 'POST':
        star_rating = request.POST.get('star_rating')
        comment = request.POST.get('comment')

        if (star_rating and comment):
                Review.objects.create(
                book=book,
                user=request.user,
                star_rating=star_rating,
                comment=comment,
        )

<<<<<<< HEAD
    return redirect(f'/books/{book_isbn}/')
=======
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'user': request.user.username,
                'star_rating': star_rating,
                'comment': comment,
            })

    return redirect('library:book_detail', isbn=book_isbn)
>>>>>>> 2e66cce06b69862adba2589a33f57b60aa18b52d



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
    num_lists = lists.count()
    read_history = lists.filter(list_type='read').first()
    wishlist = lists.filter(list_type='wishlist').first()

    return render(request, 'library/profile.html', {
        'user': user,
        'lists': lists,
        'num_lists':num_lists,
        'read_history': read_history,
        'wishlist': wishlist,
        'books_read': read_history.books.count() if read_history else 0,
        'review_count': Review.objects.filter(user=user).count(),
    })
@login_required
def list_detail_view(request, list_id):
    book_list = get_object_or_404(BookList, id=list_id, user=request.user)
    books = book_list.books.all()
    return render(request, 'library/list_detail.html', {
        'book_list': book_list,
        'books': books,
    })
@login_required
def create_new_list(request):
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        if list_name:
            BookList.objects.create(
                user=request.user,
                list_name=list_name,
                list_type='custom'
            )
            
    return redirect(request.META.get('HTTP_REFERER', 'library:profile'))

@login_required
def create_list_with_book(request,book_isbn):
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        if list_name:
            book = get_object_or_404(Book, isbn=book_isbn)
            new_list =BookList.objects.create(
                user=request.user,
                list_name=list_name,
                list_type='custom'
            )
            new_list.books.add(book)
    return redirect(request.META.get('HTTP_REFERER', 'library:profile'))
@login_required 
def remove_list(request,list_id):
    if request.method == 'POST':
        BookList.objects.filter(user=request.user, id=list_id).delete()
        return redirect('library:profile')
@login_required
def add_to_list(request, list_id, book_isbn):
    book_list = get_object_or_404(BookList, id=list_id, user=request.user)
    book = get_object_or_404(Book, isbn=book_isbn)
    book_list.books.add(book)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect(request.META.get('HTTP_REFERER', 'browse'))

@login_required
def remove_book_from_list(request, list_id, book_isbn):
    book_list = get_object_or_404(BookList, id=list_id, user=request.user)
    book = get_object_or_404(Book, isbn=book_isbn)
    book_list.books.remove(book)

    return redirect('library:list_detail', list_id=list_id)


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

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
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
    active_tab = request.GET.get('tab', 'login')
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'register':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            role = request.POST.get('role', 'student')
            avatar = request.POST.get('avatar')
            
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect(f"{reverse('library:login')}?tab=register")
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return redirect(f"{reverse('library:login')}?tab=register")
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return redirect(f"{reverse('library:login')}?tab=register")
            user = User.objects.create_user(username=username, email=email, password=password1)
            if avatar:
                user.avatar = avatar
            user.role = role
            user.save()
            login(request, user)
            return redirect('library:browse')
        
        elif form_type == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('library:browse')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect(f"{reverse('library:login')}?tab=login")
    
    return render(request, 'library/login.html', {'active_tab': active_tab})

def user_logout_view(request):
    logout(request)
    return redirect('library:browse')

@login_required
def my_books_view(request):
    lists = BookList.objects.filter(user=request.user)
    selected_id = request.GET.get('list')
    if selected_id:
        active_list = get_object_or_404(BookList, id=selected_id, user=request.user)
    else:
        active_list = lists.filter(list_type='read').first()
    books = active_list.books.all() if active_list else []
    return render(request, 'library/my_books.html', {
        'lists': lists,
        'active_list': active_list,
        'books': books,
    })
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        avatar = request.FILES.get('avatar')

        user = request.user

        if username:
            user.username = username
        if email:
            user.email = email
        if avatar:
            user.avatar = avatar
        if password1 and password2:
            if password1 == password2:
                user.set_password(password1)
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('library:edit_profile')

        user.save()
        update_session_auth_hash(request, user)
        return redirect('library:profile')

    return render(request, 'library/edit_profile.html')

