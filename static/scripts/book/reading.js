const win = document.getElementById('window')
win.style.cssText = `display: flex;`
const bookHeight = win.offsetHeight * 0.85
const bookWidth = bookHeight * 0.7142

const bookContainer = document.getElementById('book')

bookContainer.style.cssText = `margin: auto;`

class Book {
  constructor(renderContainer, name, authors, data) {
    this.blocks = data
    this.pageCounter = 0
    this.book = renderContainer
    this.name = name
    this.authors = authors
    this.containerHeight = null
    this.isPrevious = false
    this.currentBlock = this.blocks[this.blocks.length - 1]
    this.blocksHeight = 0
    this.footnoteCounter = 1
  }

  renderPages() {
    if (!this.blocks.length) return

    while (this.blocks.length) {
      this.currentBlock = this.blocks[this.blocks.length - 1]

      if (this.currentBlock.classes.includes('footnote')) {
        const block = this.renderContent(this.blocks.pop(), document.getElementById('footnotes'))
        block.id = `footnote_${this.footnoteCounter}`
        this.footnoteCounter++
        continue
      }

      const page = this.renderPage()

      if (this.currentBlock.classes.includes('cover')) {
        this.renderCover(page)
      } else if (this.currentBlock.classes.includes('chapter-header')) {
        this.renderChapter(page)
      } else {
        const contentBlock = this.renderGrid(page)
        if (this.currentBlock.classes.includes('chapter-title')) {
          this.renderTitle(contentBlock)
        }

        while (this.blocks.length) {
          this.currentBlock = this.blocks[this.blocks.length - 1]
          if (['cover', 'chapter-header', 'chapter-title', 'footnote'].some(className => this.currentBlock.classes.includes(className))) {
            break
          }

          const block = this.blocks.pop()
          const renderedBlock = this.renderContent(block, contentBlock)

          if (this.isPrevious) {
            renderedBlock.style.textIndent = '0'
            this.isPrevious = false
          }

          if (this.blocksHeight + renderedBlock.clientHeight > this.containerHeight) {
            block.innerHTML = this.truncateContent(renderedBlock)
            this.blocks.push(block)
            this.blocksHeight = 0
            break
          } else {
            this.blocksHeight += renderedBlock.clientHeight
          }
        }
      }
      this.pageCounter++
    }
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
      classes: 'page dark:bg-gray-700 dark:text-gray-200',
      cssText: `width: ${bookWidth}px; height: ${bookHeight}px;`
    })
    this.book.appendChild(pageTag)
    return pageTag
  }

  getContainerSize(grid, header, footer) {
    const gridStyles = getComputedStyle(grid)
    const headerStyles = getComputedStyle(header)
    const footerStyles = getComputedStyle(footer)

    const gridHeight = parseInt(gridStyles.height)
    const rowGap = parseFloat(gridStyles.rowGap)
    const headerLineHeight = parseInt(headerStyles.lineHeight)
    const footerLineHeight = parseInt(footerStyles.lineHeight)
    this.containerHeight = gridHeight - rowGap * 2 - headerLineHeight - footerLineHeight

    const gridWidth = parseInt(gridStyles.width)
    const style = document.createElement('style')
    style.innerHTML = `.page .page-content {width: ${gridWidth}px !important;}`
    document.head.appendChild(style)
  }

  renderCover(page) {
    const {tagName, id, src, alt, classes} = this.blocks.pop()
    const imgTag = this.createTag({tagName, id, src, alt, classes})
    page.appendChild(imgTag)
  }

  renderChapter(page) {
    const gridTag = this.createTag({
      tagName: 'div',
      classes: 'page-content',
      cssText: 'display: flex; height: 100%; justify-content: center; flex-direction: column;'
    })

    const {tagName, id, classes, cssText, innerHTML} = this.blocks.pop()
    const headerTag = this.createTag({tagName, id, classes, cssText, innerHTML})
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

  renderGrid(page) {
    const gridTag = this.createTag({
      tagName: 'div',
      classes: 'grid h-full',
      cssText: 'grid-template-rows: 15px auto 20px; row-gap: 1rem;'
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
      innerHTML: this.pageCounter
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
    this.blocksHeight = titleTag.clientHeight
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
  return parseInt(parent.id.match(/\d+/)[0])
}

const book = new Book(bookContainer, BOOK_NAME, AUTHORS, data)

window.addEventListener('DOMContentLoaded', () => {
  bookContainer.innerHTML = ''
  book.renderPages()
  const pageFlip = new St.PageFlip(document.getElementById('book'), {
    width: bookWidth,
    height: bookHeight,
    drawShadow: true,
    autoSize: false,
    mobileScrollSupport: false,
    showCover: showCover,
    startPage: setStartPage(START),
  })

  const PGS = document.querySelectorAll('.page')
  pageFlip.loadFromHTML(PGS)
})

function submit(id) {
  $.ajax({
    type: 'POST',
    data: {
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
      content: id,
    },
    dataType: 'json',
  })
}
