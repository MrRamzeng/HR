from django.shortcuts import render, redirect

from .forms import UpdatePosition
from .models import Book, Content, UserBooks, BookPage


def index(request):
    return render(request, 'book/index.html')


def books(request):
    books = Book.objects.all()
    return render(
        request,
        'book/books.html',
        {
            'books': books
        }
    )


def book(request, id):
    book = Book.objects.get(id=id)
    return render(
        request,
        'book/book.html',
        {
            'book': book
        }
    )


def add_book(request, book_id):
    UserBooks.objects.get_or_create(
        user_id=request.user.id,
        book_id=book_id
    )
    return redirect('user_books')


def user_books(request):
    books = UserBooks.objects.filter(user_id=request.user.id)
    return render(
        request,
        'book/user_books.html',
        {
            'books': books
        }
    )


def reading(request, book_id):
    book = UserBooks.objects.get(book_id=book_id, user_id=request.user.id)
    if book.has_read:
        return redirect('user_books')
    if request.method == 'POST':
        form = UpdatePosition(request.POST)
        if form.is_valid():
            book.page_position = form.cleaned_data.get('position')
            if book.page_position >= book.get_pages_count():
                book.has_read = True
            book.save()
            return redirect('reading', book_id)
    else:
        form = UpdatePosition(
            initial={
                'position': book.page_position
            }
        )

    # pages = book.pages.all()[book.page:book.page + 2]
    pages = BookPage.objects.filter(
        book_id=book_id
    )[book.page_position:book.page_position + 2]
    return render(
        request,
        'book/reading.html',
        {
            'pages': pages,
            'form': form,
            'pages_count': book.get_pages_count()
        }
    )


def set_part(contents):
    part = []
    symbols = 1997
    for content in contents:
        if symbols > len(content.text):
            slice_content(part, content)
            symbols -= len(content.text)
        else:
            slice_content(part, content, symbols)
            break
    return part


def slice_content(lst, content, slice=0):
    lst.append(
        {
            'tag': content.type.tag,
            'css': content.type.css,
            'src': content.type.src,
            'text': content.text[:slice] + '...' if slice else content.text
        }
    )


def printing(request, book_id):
    book = UserBooks.objects.get(book_id=book_id, user_id=request.user.id)
    if book.has_print:
        return redirect('user_books')
    if request.method == 'POST':
        form = UpdatePosition(request.POST)
        if form.is_valid():
            book.print_position = form.cleaned_data.get('position')
            if book.get_print_progress() == 100:
                book.has_print = True
            book.save()
            return redirect('printing', book_id)
    else:
        form = UpdatePosition(
            initial={
                'position': book.print_position
            }
        )

    contents = Content.objects.filter(type__book_id=book_id)[book.print_position:]
    part = set_part(contents)
    return render(
        request,
        'book/printing.html',
        {
            'form': form,
            'contents': part
        }
    )
