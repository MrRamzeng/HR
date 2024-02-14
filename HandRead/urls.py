from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('books/', views.books, name='books'),
    path('book/<int:id>/', views.book, name='book'),
    path('add_book/<int:book_id>/', views.add_book, name='add_book'),
    path('my_books/', views.user_books, name='user_books'),
    path('book/<int:book_id>/printing/', views.printing, name='printing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
