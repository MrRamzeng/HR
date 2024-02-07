from django.shortcuts import render
from .models import Book


def index(request):
    return render(request, 'index.html')


def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


def book(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'book.html', {'book': book})
