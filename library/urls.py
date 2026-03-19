from django.urls import path
from library import views

app_name = 'library'

urlpatterns = [
    path('browse/', views.browse_view, name='browse'),
    path('search/', views.search_view, name='search'),
    path('books/<str:isbn>/', views.book_detail_view, name='book_detail'),
    path('books/<str:book_isbn>/mark-as-read/', views.mark_as_read, name='mark_as_read'),   
    path('lists/<int:list_id>/add/<str:book_isbn>/', views.add_to_list, name='add_to_list'),
    path('lists/create-new',views.create_new_list, name = 'create_new_list' ) ,
    path('lists/create/<str:book_isbn>/', views.create_list_with_book, name='create_list_with_book'),
    path('lists/<int:list_id>/', views.list_detail_view, name='list_detail'),
    path('lists/delete/<int:list_id>/', views.remove_list , name ='remove_list' ),
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