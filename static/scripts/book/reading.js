const footnotesBlock = document.getElementById('footnotes')

const bookContainer = document.getElementById('book');

const sideBlock = document.getElementById('side_nav')
const PROGRESS = document.getElementById('progress')

bookContainer.style.height = `${(win.offsetHeight - parseInt(winStyles.padding) * 2) * .9}px`
bookContainer.style.width = `${(win.offsetHeight - parseInt(winStyles.padding) * 2) * .9 * .7142}px`

document.getElementById('cover').style.cssText += `max-width: ${bookContainer.offsetWidth}px; width: ${bookContainer.offsetWidth}px;`
const pageWidth = bookContainer.offsetWidth

function calcBookWidth() {
  win.style.width = `${document.body.offsetWidth - parseInt(winStyles.marginLeft)}px`
  bookContainer.style.width = `${win.offsetWidth - parseInt(winStyles.padding) * 2 < (pageWidth + 5) * 2 ? pageWidth : pageWidth * 2}px`;
}

const end = document.getElementById('end_book')

for (const footnote of footnotes) {
  footnotesBlock.innerHTML += footnote
}

class Book {
  constructor(renderContainer, name, authors, data, start) {
    this.blocks = [...data]
    this.pageCounter = 0
    this.book = renderContainer
    this.name = name
    this.authors = authors
    this.currentBlockId = +start
    this.chapterCounter = 0

    this.containerHeight = null
    this.isPrevious = false
    this.currentBlock = this.blocks[this.blocks.length - 1]
    this.blocksHeight = 0
  }

  renderPages() {
    if (!this.blocks.length) return;

    const fragment = document.createDocumentFragment();
    while (this.blocks.length) {
      this.currentBlock = this.blocks[this.blocks.length - 1];
      const page = this.renderPage();

      if (this.currentBlock.classes.includes('chapter-header')) {
        this.renderChapter(page);
      } else {
        const contentBlock = this.renderGrid(page);

        if (this.currentBlock.classes.includes('chapter-title')) {
          this.renderTitle(contentBlock);
        }

        while (this.blocks.length) {
          this.currentBlock = this.blocks[this.blocks.length - 1];
          if (['chapter-header', 'chapter-title', 'footnote'].some(className => this.currentBlock.classes.includes(className))) {
            break;
          }

          const block = this.blocks.pop();
          const renderedBlock = this.renderContent(block, contentBlock);

          if (this.isPrevious) {
            renderedBlock.style.textIndent = '0';
            this.isPrevious = false;
          }

          if (this.blocksHeight + renderedBlock.clientHeight > this.containerHeight) {
            block.innerHTML = this.truncateContent(renderedBlock);
            this.blocks.push(block);
            this.blocksHeight = 0;
            break;
          } else {
            this.blocksHeight += renderedBlock.clientHeight;
          }
        }
      }
      fragment.appendChild(page);
      page.style.display = 'none';
      this.pageCounter++;
    }
    this.book.insertBefore(fragment, end);
    end.id = this.pageCounter;
  }

  createTag({tagName, id, src, alt, classes, cssText, innerHTML}) {
    const tag = document.createElement(tagName)
    if (id) tag.id = id
    if (src) tag.src = src
    if (alt) tag.alt = alt
    if (classes) tag.className = classes
    if (cssText) tag.style.cssText = cssText
    if (innerHTML) tag.innerHTML = innerHTML
    return tag
  }

  renderPage() {
    const pageTag = this.createTag({
      tagName: 'section',
      id: `section_${this.pageCounter}`,
      classes: 'page dark:page',
      cssText: `width: ${pageWidth}px; height: ${bookContainer.offsetHeight}px;`
    })
    this.book.appendChild(pageTag)
    return pageTag
  }

  getContainerSize(grid, header, footer) {
    const gridStyles = getComputedStyle(grid)
    const rowGap = parseFloat(gridStyles.rowGap) * 2
    const pageStyles = getComputedStyle(grid.closest('.page'))
    const pagePadding = parseInt(pageStyles.padding) * 2
    const pageBorder = parseInt(pageStyles.borderWidth) * 2


    const gridHeight = bookContainer.offsetHeight - pagePadding - pageBorder

    const headerStyles = getComputedStyle(header)
    const footerStyles = getComputedStyle(footer)
    const headerLineHeight = parseInt(headerStyles.lineHeight)
    const footerLineHeight = parseInt(footerStyles.lineHeight)
    this.containerHeight = gridHeight - rowGap - headerLineHeight - footerLineHeight

    const gridWidth = parseInt(gridStyles.width)
    const style = document.createElement('style')
    style.innerHTML = `.page-content {width: ${gridWidth}px !important; height: ${this.containerHeight}px;`
    document.head.appendChild(style)
  }

  renderChapter(page) {
    const gridTag = this.createTag({
      tagName: 'div',
      classes: 'page-content',
      cssText: 'display: flex; height: 100%; justify-content: center; flex-direction: column;'
    })
    const {tagName, id, classes, cssText, innerHTML} = this.blocks.pop()
    const headerTag = this.createTag({tagName, id, classes, cssText, innerHTML})
    this.renderChapterToSidebar(page.id.match(/\d+/)[0], innerHTML)
    this.currentBlock = this.blocks[this.blocks.length - 1]
    if (this.currentBlock.tagName === 'signature') {
      const {tagName, id, cssText, innerHTML} = this.blocks.pop()
      const signatureTag = this.createTag({tagName, id, cssText, innerHTML})
      gridTag.append(headerTag, signatureTag)
    } else {
      gridTag.appendChild(headerTag)
    }
    page.appendChild(gridTag)
  }

  renderChapterToSidebar(pageId, title) {
    this.chapterCounter++
    const chapterTag = this.createTag({
      tagName: 'li',
      innerHTML: `
      <button type="button" onclick="chapterClick(event)" class="flex items-center w-full p-2 text-base text-gray-900 transition duration-75 rounded-lg group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700" aria-controls="chapter_${this.chapterCounter}" data-collapse-toggle="chapter_${this.chapterCounter}">
        <span class="flex-1 ms-3 text-left rtl:text-right">${title}</span>
        <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
           <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
        </svg>
      </button>
      <ul id="chapter_${this.chapterCounter}" class="hidden py-2 space-y-2">
        <li class="p-3 text-gray-900 rounded-lg dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 group border-b dark:border-gray-700" onclick="pageFlip.flip(${pageId})">
          ${title}
        </li>
      </ul>
      `
    })
    sideBlock.appendChild(chapterTag)
  }

  renderGrid(page) {
    const gridTag = this.createTag({
      tagName: 'div',
      classes: 'grid gap-y-4',
      cssText: 'grid-template-rows: 15px 1fr 20px;'
    })

    const headerTag = this.createTag({
      tagName: 'div',
      classes: 'header',
      innerHTML: this.pageCounter % 2 ? this.name : this.authors
    })

    const contentTag = this.createTag({
      tagName: 'div',
      classes: 'page-content'
    })

    const footerTag = this.createTag({
      tagName: 'div',
      classes: 'page-number',
      innerHTML: this.pageCounter + 1
    })

    gridTag.append(headerTag, contentTag, footerTag)
    page.appendChild(gridTag)

    if (!this.containerHeight) {
      this.getContainerSize(gridTag, headerTag, footerTag)
    }

    return contentTag
  }

  renderTitle(container) {
    const {tagName, id, classes, cssText, innerHTML} = this.blocks.pop()
    const titleTag = this.createTag({tagName, id, classes, cssText, innerHTML})
    container.appendChild(titleTag)
    this.renderTitleToSidebar(id, innerHTML)
    this.blocksHeight = titleTag.clientHeight
  }

  renderTitleToSidebar(blockId, title) {
    const contentTag = this.createTag({
      tagName: 'li',
      classes: `
        p-3 text-gray-800 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700
        group border-b dark:border-gray-700
      `,
      innerHTML: title
    })
    contentTag.onclick = () => turnTo(blockId)
    if (this.chapterCounter) {
      document.getElementById(`chapter_${this.chapterCounter}`).appendChild(contentTag)
    } else {
      sideBlock.appendChild(contentTag)
    }
  }

  renderContent(block, container) {
    const {tagName, id, src, alt, classes, cssText, innerHTML} = block
    const blockTag = this.createTag({tagName, id, src, alt, classes, cssText, innerHTML})
    container.appendChild(blockTag)
    return blockTag
  }

  truncateContent(block) {
    const content = block.innerHTML.match(/<[^>]+>|[^\s<]+/g);
    const truncatedContent = []
    const remainingContent = []
    block.innerHTML = ''
    for (let i = 0; i < content.length; i++) {
      let word = content[i]
      block.innerHTML += truncatedContent.length ? ` ${word}` : word

      if (this.blocksHeight + block.clientHeight > this.containerHeight) {
        block.innerHTML = truncatedContent.join(' ')
        if (truncatedContent.length > 0) {
          this.isPrevious = true
        }
        remainingContent.push(...content.slice(i))
        break
      }
      truncatedContent.push(word)
    }
    return remainingContent.join(' ')
  }
}

function lastContentId(page) {
  const contentElements = Array.from(page.querySelectorAll('[id]')).filter(element => /^\d+$/.test(element.id))
  return contentElements[contentElements.length - 1].id
}

function setStartPage(searchId) {
  const content = document.getElementById(searchId)
  const parent = content.closest('.page')
  return +(parent.id.match(/\d+/)[0])
}

const book = new Book(bookContainer, BOOK_NAME, AUTHORS, data, START)

let pageFlip

book.renderPages()

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('cover').style.opacity = '0'
  pageFlip = new St.PageFlip(document.getElementById('book'), {
    width: bookContainer.offsetWidth,
    height: bookContainer.offsetHeight,
    drawShadow: true,
    autoSize: true,
    mobileScrollSupport: false,
    showCover: false,
    startPage: setStartPage(book.currentBlockId),
  });
  PROGRESS.style.width = `${(book.currentBlockId / data.length) * 100}%`;
  pageFlip.loadFromHTML(document.querySelectorAll('.page'))
  calcBookWidth()
  setTimeout(() => document.getElementById('book').classList.add('visible'), 1);
});

// Троттлинг для `resize` события
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(calcBookWidth, 100);
});

function chapterClick(e) {
  const btn = e.target.closest('button')
  btn.querySelector("svg").classList.toggle('rotate-180')
}

function turnTo(blockId) {
  const startPage = setStartPage(blockId)

  pageFlip.flip(startPage)
  submit(blockId)
}

function removeClasses(element) {
  const classesToRemove = Array.from(
    element.classList
  ).filter(className => className.includes("bg"))
  classesToRemove.forEach(className => element.classList.remove(className));
}

function submit(val) {
  $.ajax({
    type: 'POST',
    data: {
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
      content: val,
    },
    dataType: 'json',
    success: function(response){
      if (response.status === 'redirect') {
        window.location.href = response.redirect;  // Перенаправляем пользователя
      }
      if (response.status === 'success') {
        PROGRESS.style.width = `${response.blocks / data.length * 100}%`
        book.currentBlockId = response.blocks
      }
    },
  })

}
