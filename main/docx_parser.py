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
    blocks = doc.paragraphs
    trunc_text = False
    for block in blocks:
        text_len = len(block.text.strip())
        text = ''
        style = ''
        css = ''
        if block.text == '':
            data[-1]['text'] += '<br>'

        for run in block.runs:
            content = run.text.replace('\n', '<br>')
            if run.italic:
                content = f'<i>{content}</i>'
            if run.bold:
                text += f'<b>{content}</b>'
            else:
                text += content

        if block.style.name == 'Subtitle':
            tag = 'img'
            css += 'cover'
            text_len = 0
        elif block.style.name == 'Title':
            tag = 'header'
            css = 'chapter-header dark:chapter-header'
        elif block.style.name == 'Signature':
            tag = 'signature'
        elif block.style.name == 'Heading 1':
            tag = 'h1'
            css = 'chapter-title dark:chapter-title'
        elif block.style.name == 'Caption':
            note = (
                f'<strong>{text}</strong>'
            )
            data[-1]['text'] += note
            trunc_text = True
            continue
        elif block.style.name == 'footnote text':
            continue
        elif block.style.name == 'Body Text':
            if trunc_text:
                data[-1]['text'] += f' {text}'
                trunc_text = False
                continue
            tag = 'p'
        else:
            if trunc_text:
                data[-1]['text'] += f' {text}'
                trunc_text = False
                continue
            tag = 'i'

        if block.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.CENTER:
            style += 'text-align: center;'
        elif block.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.RIGHT:
            style += 'text-align: right; '
        elif (block.style.paragraph_format.alignment ==
              WD_ALIGN_PARAGRAPH.JUSTIFY):
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
    return data
