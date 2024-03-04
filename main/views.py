from django.shortcuts import render, redirect

from .forms import UpdatePosition, UpdatePagePosition
from .models import Book, Content, Reading, BookPage


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
    pages = BookPage.objects.filter(
        book_id=book_id
    ).values_list(
        'id', flat=True
    )
    r, created = Reading.objects.get_or_create(
        user_id=request.user.id,
        book_id=book_id
    )
    if created:
        r.pages.add(*pages)
    return redirect('user_books', book_id=book_id)


def user_books(request):
    books = Reading.objects.filter(user_id=request.user.id)
    return render(
        request,
        'user_books.html',
        {
            'books': books
        }
    )


def reading(request, book_id):
    book = Reading.objects.get(book_id=book_id, user_id=request.user.id)
    pages = book.pages.all()[book.page:book.page + 2]
    if request.method == 'POST':
        form = UpdatePagePosition(request.POST)
        if form.is_valid():
            book.page = form.cleaned_data.get('position')
            book.has_read = form.cleaned_data.get('has_read')
            book.save()
            return redirect('reading', book_id)
    else:
        form = UpdatePagePosition(
            initial={
                'position': book.page
            }
        )
    if book.has_read:
        return redirect('user_books')
    return render(
        request,
        'reading.html',
        {
            'pages': pages,
            'form': form,
            'book': book
        }
    )


def printing(request, book_id):
    contents = Content.objects.filter(
        type__book_id=book_id
    ).values_list(
        'id', flat=True
    )
    book, created = Reading.objects.get_or_create(book_id=book_id,
        user_id=request.user.id)
    book.contents.add(*contents)
    if request.method == 'POST':
        form = UpdatePosition(request.POST)
        if form.is_valid():
            book.position = form.cleaned_data.get('position')
            book.contents.remove(book.contents.first().id)
            book.save()
            return redirect('user_books') if not book.contents else redirect(
                'printing', book_id
            )
    else:
        form = UpdatePosition(
            initial={
                'position': book.position
            }
        )
    contents = book.contents.all()
    if contents:
        return render(
            request,
            'printing.html',
            {
                'form': form,
                'contents': contents
            }
        )
    return redirect('user_books')
