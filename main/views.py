from django.shortcuts import render, redirect

from .forms import UpdatePosition
from .models import Book, Content, Printing


def index(request):
    return render(request, 'index.html')


def books(request):
    books = Book.objects.all()
    return render(
        request,
        'books.html',
        {
            'books': books
        }
    )


def book(request, id):
    book = Book.objects.get(id=id)
    return render(
        request,
        'book.html',
        {
            'book': book
        }
    )


def add_book(request, book_id):
    content = Content.objects.filter(
        tag__book_id=book_id
    ).values_list(
        'id',
        flat=True
    )
    p, created = Printing.objects.get_or_create(
        user_id=request.user.id,
        book_id=book_id
    )
    p.content.add(*content)
    p.save()
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
    if request.method == 'POST':
        form = UpdatePosition(request.POST)
        if form.is_valid():
            book.position = form.cleaned_data.get('position')
            book.content.remove(book.content.first().id)
            book.save()
            return redirect('user_books') if not book.content else redirect(
                'printing', book_id
            )
    else:
        form = UpdatePosition(
            initial={
                'position': book.position
            }
        )
    content = book.content.all()
    return render(
        request,
        'printing.html',
        {
            'form': form,
            'content': content
        }
    ) if content else redirect('user_books')
