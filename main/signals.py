from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BookFile, Content


@receiver(post_save, sender=BookFile)
def update_book_content(instance, **kwargs):
    # Проверяем, что файл является .docx
    if instance.file.path.endswith('.docx'):
        data = instance.extract_content()
        if data:
            for content in data:
                Content.objects.update_or_create(
                    book=instance.book,
                    text=content['text'],
                    text_len=content['text_len'],
                    css=content['css'],
                    tag=content['tag'],
                    style=content['style'],
                )