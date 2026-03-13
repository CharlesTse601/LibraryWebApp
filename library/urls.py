from django.urls import path
from library import views

app_name = 'library'

urlpatterns = [
    path('browse/', views.browse_view, name='browse'),
    path('search/', views.search_view, name='search'),
    path('categories/', views.category_list_view, name='categories'),
    path('categories/<str:category_name>/', views.category_detail_view, name='category_detail'),
    path('categories/<str:category_name>/<str:book_isbn>/', views.book_detail_view, name='book_detail'),
    path('recentlypublished/', views.recently_published_view, name='recently_published'),
    path('aboutus/', views.about_us_view, name='about_us'),
    path('FAQ/', views.faq_view, name='faq'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('login/myaccount/', views.profile_view, name='profile'),
    path('login/myaccount/mybooks/', views.my_books_view, name='my_books'),
]