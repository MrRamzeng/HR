from django.shortcuts import render, redirect

from .forms import UpdatePosition
from .models import Book, Printing


def index(request):
    return render(request, 'index.html')


def books(request):
    books = Book.objects.all()
    return render(
        request, 'books.html', {
            'books': books
        }
    )


def book(request, id):
    book = Book.objects.get(id=id)
    return render(
        request, 'book.html', {
            'book': book
        }
    )


def add_book(request, book_id):
    Printing.objects.get_or_create(user_id=request.user.id, book_id=book_id)
    return redirect('printing', book_id=book_id)


def user_books(request):
    books = Printing.objects.filter(user_id=request.user.id)
    return render(
        request,
        'user_books.html',
        {
            'books': books
        }
    )


def printing(request, book_id):
    book = Printing.objects.get(book_id=book_id, user_id=request.user.id)
    print(len(book.book.tags()))
    if request.method == 'POST':
        form = UpdatePosition(request.POST)
        if form.is_valid():
            book.position = form.cleaned_data.get('position')
            book.is_finished = form.cleaned_data.get('is_finished')
            book.save()
            return redirect('user_books') if book.position == len(
                book.book.text
            ) else redirect('printing', book_id)
    else:
        form = UpdatePosition(
            initial={
                'position': book.position
            }
        )
    return redirect('user_books') if book.is_finished else render(
        request,
        'printing.html',
        {
            'form': form,
            'book': book
        }
    )
