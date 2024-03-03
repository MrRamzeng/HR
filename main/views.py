from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView, UpdateAPIView

from .forms import UpdatePosition, UpdatePagePosition
from .models import Book, Content, Printing, Reading, BookPage
from .serializer import BooksSerializer


def index(request):
    return render(request, 'index.html')


class BooksAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer


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
        type__book_id=book_id
    ).values_list(
        'id',
        flat=True
    )
    p, created = Printing.objects.get_or_create(
        user_id=request.user.id,
        book_id=book_id
    )
    r, created = Reading.objects.get_or_create(user_id=request.user.id,
        book_id=book_id)
    if created:
        r.pages.add(*BookPage.objects.filter(book_id=book_id).values_list('id',
            flat=True)
        )
        p.content.add(*content)
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


def reading(request, book_id):
    book = Reading.objects.get(book_id=book_id, user_id=request.user.id)
    pages = book.pages.all()[book.page:book.page + 2]
    print(pages)
    if request.method == 'POST':
        form = UpdatePagePosition(request.POST)
        if form.is_valid():
            book.page = form.cleaned_data.get('position')
            book.is_finished = form.cleaned_data.get('is_finished')
            book.save()
            return redirect('reading', book_id)
    else:
        form = UpdatePagePosition(
            initial={
                'position': book.page
            }
        )
    if book.is_finished:
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


# class Print(UpdateAPIView):
#     get
#     queryset = Printing.objects.get(book_id=book_id, user_id=req)


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
