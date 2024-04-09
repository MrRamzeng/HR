from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/<int:id>/', views.book, name='book'),
    path('books/add/<int:book_id>/', views.add_book, name='add_book'),
    path('books/<int:book_id>/reading/', views.reading, name='reading'),
    path('books/<int:book_id>/typing/', views.typing, name='typing'),
    path('books/', views.books, name='books'),
    path('books/my', views.user_books, name='user_books'),
    path('authors/<int:id>/', views.author, name='author'),
    path('authors/', views.authors, name='authors')
]
