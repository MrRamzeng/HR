from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

def process_text(paragraph, text):
    """Обработка текста и добавление к последнему элементу списка"""
    if 'footnote' in paragraph:
        return f' {text}' if text[0].isalpha() else text
    raise ValueError


def extract_word_data(file_path):
    doc = Document(file_path)
    data = []
    ps = doc.paragraphs[:15]
    for paragraph in ps:
        # print(paragraph.text[:50])
        text_len = len(paragraph.text.strip())
        text = ''
        style = ''
        css = ''
        if paragraph.text == '':
            data[-1]['text'] += '<br>'

        for run in paragraph.runs:
            content = run.text.replace('\n', '<br>')
            if run.italic:
                content = f'<i>{content}</i>'
            if run.bold:
                text += f'<b>{content}</b>'
            else:
                text += content

        if paragraph.style.name == 'Subtitle':
            tag = 'img'
            css += 'cover'
            text_len = 0
        elif paragraph.style.name == 'Title':
            tag = 'header'
            css = 'chapter-header dark:chapter-header'
        elif paragraph.style.name == 'Signature':
            tag = 'signature'
        elif paragraph.style.name == 'Heading 1':
            tag = 'h1'
            css = 'chapter-title dark:chapter-title'
        elif paragraph.style.name == 'Caption':
            note = f'<footnote-t title="{text}"></footnote-t>'
            data[-1]['text'] += note
            continue
        elif paragraph.style.name == 'footnote text':
            tag = 'p'
            text = f'<footnote-c text="{text}"></footnote-c>'
        elif paragraph.style.name == 'Body Text':
            tag = 'p'
        else:
            tag = 'i'

        if paragraph.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.CENTER:
            style += 'text-align: center;'
        elif paragraph.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.RIGHT:
            style += 'text-align: right; '
        elif paragraph.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY:
            style += 'text-align: justify;'
        if text:
            data.append(
                {
                    'tag': tag,
                    'css': css,
                    'src': '',
                    'style': style,
                    'text': text,
                    'text_len': text_len,
                }
            )
    # print(json.dumps(data, indent=4, ensure_ascii=False))
    return data
# extract_word_data('media/книги/Жизнь_пи/Файл_книги/Пи.docx')