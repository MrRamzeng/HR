from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH


def extract_word_data(file_path):
    doc = Document(file_path)
    data = []

    for paragraph in doc.paragraphs:
        text_len = len(paragraph.text.strip())
        text = ''
        style = ''
        css = ''

        for run in paragraph.runs:
            content = run.text.replace('\n', '<br>')
            if run.italic:
                content = f'<i>{content}</i>'
            if run.bold:
                text += f'<b>{content}</b>'
            else:
                text += content

        if paragraph.style.name == 'Title':
            tag = 'h1'
            css += 'chapter '
        elif paragraph.style.name == 'Heading 1':
            tag = 'h2'
        elif paragraph.style.name == 'Heading 2':
            tag = 'h3'
            css += 'chapter-title dark:chapter-title'
        elif paragraph.style.name == 'Subtitle':
            tag = 'img'
            css += 'cover '
            text_len = 0
        elif paragraph.style.name == 'Heading 6':
            tag = 'img'
        else:
            tag = 'p'

        if paragraph.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.CENTER:
            style += 'text-align: center;'
        elif paragraph.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.RIGHT:
            style += 'text-align: right; '
        elif paragraph.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY:
            style += 'text-align: justify;'
        if text:
            data.append(
                {
                    'text': text,
                    'text_len': text_len,
                    'css': css,
                    'src': '',
                    'tag': tag,
                    'style': style,
                }
            )
    return data
