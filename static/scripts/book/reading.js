const win = document.getElementById('window')
win.style.cssText = `width: ${win.offsetWidth}px; display: flex; justify-content: center`
const bookHeight = win.clientHeight
const bookWidth = bookHeight * 0.707


document.getElementById('book').style.cssText = `
  max-width: ${window.innerWidth < window.innerHeight ? bookWidth : bookWidth * 2 + 1}px;
  width: 100%
`

function truncateContent(block, container, maxHeight) {
  let content = block.innerHTML.split(' ')
  let end = content.length

  for (end; end > 0; end--) {
    if (container.offsetHeight < maxHeight) {
      break
    }
    block.innerHTML = content.slice(0, end).join(' ')
  }
  content = content.slice(end + 1).join(' ')

  return [content, content.length - 1]
}

function getContainerSize(grid, header, footer) {
  const gridStyles = getComputedStyle(grid)

  return parseInt(gridStyles.height) - parseInt(gridStyles.rowGap) * 2 - parseInt(getComputedStyle(header).lineHeight) - parseInt(getComputedStyle(footer).lineHeight)
}

function renderBlock(html) {
  const tag = document.createElement(html.tag)

  if (html.class) Object.assign(tag, {className: html.class})

  if (html.src) {
    Object.assign(tag, {src: `${html.src}`})
    return tag
  }

  Object.assign(tag, {innerHTML: html.content})

  return tag
}

let cut = document.querySelector('.--portrait') ? 1 : 2

function renderPage(number) {
  const section = document.createElement('section')

  Object.assign(section, {
    id: `page_${number}`,
    className: 'page dark:bg-gray-700 dark:text-gray-200',
    style: `width: ${bookWidth}px; height: ${bookHeight}px`
  })
  document.getElementById('book').appendChild(section)

  return document.getElementById(section.id)
}

function renderGrid(number, page, header, content, footer) {
  const grid = document.createElement('div')

  Object.assign(grid, {
    id: `page_grid_${number}`,
    className: 'page-content grid h-full',
    style: 'grid-template-rows: max-content auto max-content; row-gap: 1em;'
  })
  grid.append(header, content, footer)
  page.appendChild(grid)

  return [grid, header, content, footer]
}

function createHeader(number) {
  const header = document.createElement('div')

  Object.assign(header, {
    id: `header_${number}`,
    className: 'header',
    textContent: number % 2 ? BOOK : AUTHORS
  })

  return header
}

function createContent(number) {
  const content = document.createElement('div')

  Object.assign(content, {
    id: `content_${number}`,
    className: 'page-content'
  })

  return content
}

function createFooter(number) {
  const footer = document.createElement('div')

  Object.assign(footer, {
    id: `footer_${number}`,
    className: 'page-number',
    textContent: number
  })

  return footer
}

function renderBook() {
  let isPrevious = false
  let pageCounter = 0

  while (data.length) {
    const page = renderPage(pageCounter)
    let contentCounter = 0

    if (data.length >= 0 && data[data.length - 1].class === 'cover') {
      const content = data.pop()
      page.dataset.content = 1
      const img = document.createElement('img')
      Object.assign(img, {
        src: content.src,
        style: 'position: absolute; top: 0; left: 0; height 100%; width: 100%'
      })
      pageCounter++
      page.appendChild(img)
      continue
    }

    const [grid, header, contentContainer, footer] = renderGrid(
      pageCounter, page, createHeader(pageCounter), createContent(pageCounter),
      createFooter(pageCounter)
    )


    while (data.length) {
      if (data[data.length - 1].class === 'cover') break
      const content = data.pop()
      contentContainer.appendChild(renderBlock(content))
      const lastContent = contentContainer.lastElementChild

      if (isPrevious) {
        lastContent.style.textIndent = 0
        isPrevious = false
      } else {
        contentCounter++
      }

      const containerHeight = getContainerSize(grid, header, footer)

      if (contentContainer.offsetHeight > containerHeight) {
        let cut_idx
        [content['content'], cut_idx] = truncateContent(
          lastContent, contentContainer, containerHeight
        )
        !cut && ($('#cut').val(cut_idx))
        cut--
        data.push(content)
        isPrevious = true
        break
      }
    }

    page.dataset.content = contentCounter.toLocaleString()
    pageCounter++
  }
}

renderBook()

$(document).on("submit", '#read', function (e) {
  e.preventDefault()
  $.ajax({
    type: 'POST',
    data: {
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
      content: $('#content').val(),
      idx: $('#cut').val()
    },
    success: function (data) {
      $('#status').html(data)
    }
  })
})

function nextContent() {
  const contentField = $('#content')
  const pages = document.querySelectorAll('.page:not([style="display: none;"])')
  let content = 0
  for (const page of pages) {
    content += parseInt(page.dataset['content'])
  }
  contentField.val(content)
}