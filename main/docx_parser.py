from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from .models import Chapter, Content, Footnote
from django.db import transaction


def process_text(paragraph, text):
    """Обработка текста и добавление к последнему элементу списка"""
    if 'footnote' in paragraph:
        return f' {text}' if text[0].isalpha() else text
    raise ValueError


def modify_block_content(block, idx):
    footnote_title = ''
    text = ''
    for run in block.runs:
        content = run.text.replace('\n', '<br>')
        if run.italic:
            content = f'<i>{content}</i>'
        if run.bold:
            content = f'<b>{content}</b>'
        if run.underline:
            footnote_title = f'<button data-modal-target="footnote_{idx}" data-modal-toggle="footnote_{idx}" type="button">{content}'
            continue
        if run.font.superscript:
            content = f'{footnote_title}<sup>{idx}</sup></button>'
            idx += 1
        text += content
    return text, idx


def extract_word_data(file_path, book_id):
    doc = Document(file_path)
    chapter_cache = {}  # Кэш для глав, чтобы избежать многократных запросов
    footnote_counter = 1
    idx = 1
    content_cache = {}  # Кэш для Content, связанный с текущей главой

    with transaction.atomic():  # Используем транзакцию для повышения производительности и атомарности
        for content_id, block in enumerate(doc.paragraphs):
            if block.text == '':
                append_br_to_last_content(content_cache)
                continue

            text_len = len(block.text.strip())
            text, idx = modify_block_content(block, idx)
            style_name = block.style.name

            # Обработка главы
            if style_name == 'Title':
                chapter_id = get_or_create_chapter(book_id, text, chapter_cache)
                content_cache = load_content_cache_for_chapter(chapter_id)
                continue  # Пропускаем обработку контента, если это заголовок

            # Обработка сноски
            elif style_name == 'footnote text':
                footnote_text = create_footnote_html(text, footnote_counter)
                Footnote.objects.update_or_create(
                    content_id=content_id, defaults={'text': footnote_text}
                )
                footnote_counter += 1
                continue

            # Формирование данных для контента
            data = {
                'chapter_id': chapter_id,
                'text': text,
                'style': block_text_align(block),
                'text_len': text_len,
                'tag': determine_tag(style_name),
                'css': determine_css(style_name),
            }

            # Создаем контент, если он отсутствует в кэше
            content_id = get_or_create_content(data, content_cache)
            content_cache['last_content_id'] = content_id

def append_br_to_last_content(content_cache):
    """Добавляет '<br>' к последнему контенту в кэше."""
    last_content = content_cache.get('last_content')
    if last_content:
        last_content.text += '<br>'
        last_content.save(update_fields=['text'])

def get_or_create_chapter(book_id, text, chapter_cache):
    """Создает или получает главу из кэша."""
    if text not in chapter_cache:
        chapter, _ = Chapter.objects.update_or_create(book_id=book_id, name=text)
        chapter_cache[text] = chapter.id
    return chapter_cache[text]

def load_content_cache_for_chapter(chapter_id):
    """Загружает кэш контента для данной главы."""
    return {content.text: content.id for content in Content.objects.filter(chapter_id=chapter_id)}

def get_or_create_content(data, content_cache):
    """Создает контент, если его нет в кэше."""
    if data['text'] not in content_cache:
        content = Content.objects.create(**data)
        content_cache[data['text']] = content.id
    return content_cache[data['text']]

def determine_tag(style_name):
    """Определяет тег по имени стиля."""
    return {
        'Subtitle': 'img',
        'Signature': 'signature',
        'Heading 1': 'h1',
        'Body Text': 'p',
    }.get(style_name, 'i')

def determine_css(style_name):
    """Определяет CSS по имени стиля."""
    return 'chapter-title dark:chapter-title' if style_name == 'Heading 1' else ''

def create_footnote_html(text, footnote_counter):
    """Создает HTML для сноски."""
    return f'''
<div id="footnote_{footnote_counter}" class="footnote fixed top-0 left-0 right-0 z-50 hidden w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] max-h-full">
    <div class="relative w-full max-w-md max-h-full">
        <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
            <div class="flex p-3 border-b dark:border-gray-600">
                <button type="button" data-modal-hide="footnote_{footnote_counter}" class="text-gray-400 bg-transparent hover:text-gray-900 rounded-lg text-sm w-3 h-3 ms-auto dark:hover:text-white">
                    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                    </svg>
                    <span class="sr-only">Close modal</span>
                </button>
            </div>
            <div class="p-4 md:p-5 space-y-4">
                <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">{text}</p>
            </div>
        </div>
    </div>
</div>'''.strip('\n')

def block_text_align(block):
    alignment = block.style.paragraph_format.alignment
    if alignment == WD_ALIGN_PARAGRAPH.CENTER:
        return 'text-align: center;'
    elif alignment == WD_ALIGN_PARAGRAPH.RIGHT:
        return 'text-align: right;'
    elif (alignment == WD_ALIGN_PARAGRAPH.JUSTIFY
          and block.style.name != 'footnote text'):
        return 'text-align: justify;'

