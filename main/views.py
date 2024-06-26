from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from .forms import UpdatePosition
from .models import Book, Content, UserBooks, BookPage, Genre, Author


def index(request):
    books = Book.objects.filter(debug=False).only(
        'id', 'name', 'authors', 'price', 'image'
    ).order_by('-id')[:10]
    queryset = Content.objects.filter(
        type__tag='p', type__book__debug=False  # , text_len__gte=200,
        # text_len__lte=500
    ).values(
        'text', 'type__book', 'type__book__name', 'type__book__price',
        'type__book__image'
    ).order_by('?')
    print(queryset)

    return render(
        request, 'book/index.html', {
            'contents': list(queryset),
            'books': books
        }
    )


def books(request):
    return render(
        request,
        'book/books.html',
        {
            'books': Book.objects.only(
                'id', 'image', 'name', 'price', 'authors'
            ),
            'genres': Genre.objects.only('name'),
            'authors': Author.objects.only(
                'pseudonym' or ('first_name', 'last_name')
            )
        }
    )


def book(request, id):
    return render(request, 'book/book.html', {'book': Book.objects.get(id=id)})


def authors(request):
    print(dir(Author.objects.get(id=1)))
    return render(
        request,
        'book/authors.html',
        {
            'authors': Author.objects.all()
        }
    )


def author(request, id):
    return render(
        request,
        'book/author.html',
        {
            'author': Author.objects.get(id=id)
        }
    )


def add_book(request, book_id):
    UserBooks.objects.get_or_create(user_id=request.user.id, book_id=book_id)

    return redirect('user_books')


def user_books(request):
    return render(
        request,
        'book/user_books.html',
        {
            'books': UserBooks.objects.filter(user_id=request.user.id)
        }
    )


def reading(request, book_id):
    reading = UserBooks.objects.get(book_id=book_id, user_id=request.user.id)
    if reading.has_read:
        return redirect('user_books')
    if request.method == 'POST':
        reading.content_read += int(request.POST['content'])
        reading.cut_content_idx = request.POST['idx']
        reading.save()
        return HttpResponse('ok')
    content = list(
        reversed(
            Content.objects.filter(type__book_id=book_id)[reading.content_read:]
        )
    )
    return render(
        request,
        'book/reading.html',
        {
            'content': content,
            'book': reading,
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


def slice_content(lst, content, position=0):
    lst.append(
        {
            'tag': content.type.tag,
            'css': content.type.css,
            'src': content.type.src,
            'text': content.text[:position] + '...' if position else
            content.text
        }
    )


def typing(request, book_id):
    book = UserBooks.objects.get(book_id=book_id, user_id=request.user.id)
    if book.has_print:
        return redirect('user_books')

    if request.method == 'POST':
        form = UpdatePosition(request.POST)
        if form.is_valid():
            book.typing_position = form.cleaned_data.get('position')
            if book.get_print_progress() == 100:
                book.has_print = True
            book.save()
            return redirect('typing', book_id)
    else:
        form = UpdatePosition(
            initial={
                'position': book.typing_position
            }
        )

    contents = Content.objects.filter(
        type__book_id=book_id
    )[book.typing_position:]
    part = set_part(contents)

    return render(request, 'book/typing.html', {'form': form, 'contents': part})
