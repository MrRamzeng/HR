from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:id>/', views.book, name='book'),
    path('add_book/<int:book_id>/', views.add_book, name='add_book'),
    path('book/<int:book_id>/reading/', views.reading, name='reading'),
    path('book/<int:book_id>/printing/', views.printing, name='printing'),
    path('books/', views.books, name='books'),
    path('my_books/', views.user_books, name='user_books')
]
