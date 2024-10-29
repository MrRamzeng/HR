const win = document.getElementById('window')
win.style.display = 'flex';
// win.style.position = 'relative'// Проще напрямую, чем через cssText

const bookContainer = document.getElementById('book');
const bookContainerStyles = getComputedStyle(bookContainer)

const containerHeight = parseInt(bookContainerStyles.height)
const pageWidth = containerHeight * 0.7142
const progressBlock = document.getElementById('progress_block')
const PROGRESS = document.getElementById('progress')

// Кэшируем стили окна один раз
const winComputedStyle = getComputedStyle(win);

function calcWinWidth() {
  return win.clientWidth - parseInt(winComputedStyle.paddingLeft) * 2;
}

function calcBookWidth(win, pageWidth) {
  bookContainer.style.width = `${win < pageWidth * 2 ? pageWidth : pageWidth * 2}px`;
}

bookContainer.style.cssText = `height: ${containerHeight}!important; max-height: ${containerHeight}px;`

class Book {
  constructor(renderContainer, name, authors, data) {
    this.blocks = [...data]
    this.pageCounter = 0
    this.blocksCount = data.length
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
  if (!this.blocks.length) return;

  const fragment = document.createDocumentFragment();

  while (this.blocks.length) {
    this.currentBlock = this.blocks[this.blocks.length - 1];

    // Обрабатываем сноски отдельно
    if (this.currentBlock.classes.includes('footnote')) {
      const block = this.renderContent(this.blocks.pop(), document.getElementById('footnotes'));
      block.id = `footnote_${this.footnoteCounter}`;
      this.footnoteCounter++;
      continue;
    }

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
    page.style.display = 'none'
    this.pageCounter++;
  }
  this.book.appendChild(fragment);
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
      cssText: `width: ${pageWidth}px; height: ${containerHeight}px;`
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


    const gridHeight = containerHeight - pagePadding - pageBorder

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
    const progressPos = 100 - this.blocks.length / this.blocksCount * 100

    const {tagName, id, classes, cssText, innerHTML} = this.blocks.pop()
    const headerTag = this.createTag({tagName, id, classes, cssText, innerHTML})
    this.renderContentButton(progressPos, id, headerTag.innerText.replace(' ', '<br>'))
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

  renderContentButton(pos, blockId, title) {
    const contentButton = this.createTag({
      tagName: 'button',
      classes: `absolute w-3 h-3 rounded-full
      ${+blockId <= +START ? 'bg-blue-600 dark:bg-blue-500': 'bg-gray-600 dark:bg-gray-900'}`,
      cssText: `left: ${pos}%`,
      innerHTML: `<div data-popover id="popover_${blockId}" role="tooltip" class="absolute invisible inline-block w-64 text-sm text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm dark:text-gray-400 dark:border-gray-600 dark:bg-gray-800">
    <div class="px-3 py-2 bg-gray-100 border-b border-gray-200 rounded-t-lg dark:border-gray-600 dark:bg-gray-700">
        <h3 class="font-semibold text-gray-900 dark:text-white">${title}</h3>
    </div>
    <div data-popper-arrow></div>
</div>`
    })
    contentButton.onclick = () => turnTo(blockId)
    contentButton.dataset.popoverTarget = `popover_${blockId}`
    contentButton.dataset.popoverPlacement = 'bottom'
    progressBlock.appendChild(contentButton)
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
    this.blocksHeight = titleTag.clientHeight
  }

  renderContent(block, container) {
    const {tagName, id, src, alt, classes, cssText, innerHTML} = block
    const blockTag = this.createTag({tagName, id, src, alt, classes, cssText, innerHTML})
    container.appendChild(blockTag)
    document.getElementById('cover').style.opacity = `${(this.blocks.length / this.blocksCount)}`
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

const book = new Book(bookContainer, BOOK_NAME, AUTHORS, data)


book.renderPages()
const pageFlip = new St.PageFlip(document.getElementById('book'), {
  width: pageWidth,
  height: containerHeight,
  drawShadow: true,
  autoSize: true,
  mobileScrollSupport: false,
  showCover: false,
  startPage: setStartPage(START),
})

window.addEventListener('DOMContentLoaded', () => {
  // book.renderPages()
  document.getElementById('cover').style.zIndex = '0'
  PROGRESS.style.width = `${START / data.length * 100}%`
  pageFlip.loadFromHTML(document.querySelectorAll('.page'))
  calcBookWidth(calcWinWidth(), pageWidth)
  setTimeout(() => {
      document.getElementById('book').classList.add('visible');
  }, 100); // Задержка 100 мс
})

window.addEventListener('resize', () => {
  calcBookWidth(calcWinWidth(), pageWidth)
})

function turnTo(blockId) {
  pageFlip.flip(setStartPage(blockId))
  submit(blockId)
}

function removeClasses(element) {
  const classesToRemove = Array.from(element.classList).filter(className =>
    className.includes("bg")
  );
  classesToRemove.forEach(className => element.classList.remove(className));
}

function changePointBg(blockId) {
  const chapters = document.getElementsByClassName('chapter-header');

  for (const chapter of chapters) {
    const point = document.querySelector(`[data-popover-target="popover_${chapter.id}"]`);
    const isActive = +chapter.id <= +blockId;

    removeClasses(point);

    if (isActive) {
      point.classList.add('bg-blue-600', 'dark:bg-blue-500');
    } else {
      point.classList.add('bg-gray-600', 'dark:bg-gray-900');
    }
  }
}

function submit(blockId) {
  changePointBg(blockId)
  $.ajax({
    type: 'POST',
    data: {
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
      content: blockId,
    },
    dataType: 'json',
    success: function(response){
      if (response.status == 'success') {
        PROGRESS.style.width = `${response.blocks / data.length * 100}%`
      }
    },
  })
}
