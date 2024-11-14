from importlib.resources import contents

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UpdatePosition
from .models import Book, Chapter, Content, UserBooks, Genre, Author, Footnote


def index(request):
    book_list = Book.objects.filter(debug=False).only(
        'id', 'name', 'authors', 'price', 'image'
    ).order_by('-id')[:10]
    # queryset = Content.objects.filter(
    #     tag='p', book__debug=False  # , text_len__gte=200,
    #     # text_len__lte=500
    # ).values(
    #     'text', 'book', 'book__name', 'book__price',
    #     'book__image'
    # ).order_by('?')

    return render(
        request, 'book/index.html', {
            # 'contents': list(queryset),
            'books': book_list
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
    try:
        user_book = UserBooks.objects.get(
            book_id=book_id, user_id=request.user.id
        )
    except UserBooks.DoesNotExist:
        return redirect('user_books')

    if user_book.has_read:
        return redirect('user_books')

    if request.method == 'POST':
        data = request.POST.get('content')
        if data == 'was read':
            user_book.has_read = True
            user_book.content = 1
            user_book.save()

            return JsonResponse(
                {
                    'status': 'redirect',
                    'redirect': reverse('user_books')
                }
            )
        else:
            user_book.content_read = data
            user_book.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'blocks': user_book.content_read,
                }
            )
    chapters = Chapter.objects.filter(book_id=book_id)
    data = []
    footnotes = []

    for chapter in chapters:
        data.append(
            {
                'id': chapter.id,
                'text': chapter.name,
                'tag': 'header',
                'css': 'chapter-header dark:chapter-header'
            }
        )
        contents = Content.objects.filter(chapter_id=chapter.id).only(
            'id', 'tag', 'style', 'text'
        )

        for content in contents:
            data.append({
                'tag': content.tag,
                'id': content.id,
                'css': content.css,
                'style': content.style,
                'text': content.text
            })
            related_footnotes = Footnote.objects.filter(content_id=content.id)

            if related_footnotes:
                for footnote in related_footnotes:
                    footnotes.append(footnote)
    content_id = user_book.content_read

    return render(
        request,
        'book/reading.html',
        {
            'data': list(reversed(data)),
            'content_count': content_id,
            'book': user_book,
            'footnotes': footnotes
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
            'tag': content.tag,
            'css': content.css,
            'src': content.src,
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
        book_id=book_id
    )[book.typing_position:]
    part = set_part(contents)

    return render(request, 'book/typing.html', {'form': form, 'contents': part})

