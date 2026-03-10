from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def browse(request):
    return render(request, 'library/browse.html')


def search(request):
    return render(request, 'library/search.html')


def categories(request):
    return render(request, 'library/categories.html')


def category_detail(request, category_slug):
    return render(request, 'library/category_detail.html', {'category_slug': category_slug})


def book_detail(request, category_slug, book_isbn):
    return render(request, 'library/book_detail.html', {
        'category_slug': category_slug,
        'book_isbn': book_isbn,
    })


def recently_published(request):
    return render(request, 'library/recently_published.html')


def about_us(request):
    return render(request, 'library/about_us.html')


def faq(request):
    return render(request, 'library/faq.html')


def contacts(request):
    return render(request, 'library/contacts.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('library:browse')
    active_tab = request.GET.get('tab', 'login')
    return render(request, 'library/login.html', {'active_tab': active_tab})


def user_logout(request):
    logout(request)
    return redirect('library:browse')


def privacy_policy(request):
    return render(request, 'library/privacy_policy.html')


def terms_of_service(request):
    return render(request, 'library/terms_of_service.html')


@login_required
def profile(request):
    return render(request, 'library/profile.html')


@login_required
def my_books(request):
    return render(request, 'library/my_books.html')
