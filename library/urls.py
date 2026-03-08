from django.urls import path
from library import views

app_name = 'library'

urlpatterns = [
    path('browse/', views.browse, name='browse'),
    path('search/', views.search, name='search'),
    path('categories/', views.categories, name='categories'),
    path('categories/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('categories/<slug:category_slug>/<str:book_isbn>/', views.book_detail, name='book_detail'),
    path('recentlypublished/', views.recently_published, name='recently_published'),
    path('aboutus/', views.about_us, name='about_us'),
    path('FAQ/', views.faq, name='faq'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('login/myaccount/', views.profile, name='profile'),
    path('login/myaccount/mybooks/', views.my_books, name='my_books'),
]
