// theme
const themeBtn = document.getElementById('theme_toggle')
const toggleDark = document.getElementById('toggle_dark')
const toggleLight = document.getElementById('toggle_light')
// typing
const typingForm = document.getElementById('typing_form')
const previewContainer = document.getElementById('preview_container')
const textPosition = document.getElementById('id_position')
const bookTitle = document.getElementById('book_title')
const form = document.getElementById('text-form')
// accuracy game
const score = document.getElementById('id_score')
const accuracy = document.getElementById('id_accuracy')
const speed = document.getElementById('id_speed')
const timerField = document.getElementById('id_timer')
const TIMER = document.getElementById('timer')

let textBlock, caretPosition, tags, tag, marginEnd

const jsonData = document.getElementById('json_data') && JSON.parse(document.getElementById('json_data').textContent)

function init() {
  const htmlTag = document.createElement('p')
  if (jsonData) {
    const bookData = jsonData.pop()
    const bookLink = document.getElementById('book_link')
    const bookPrice = document.getElementById('book_price')
    const imgUrl = `media/${bookData['book__image']}`
    htmlTag.innerHTML = slicer(bookData['text'])
    bookLink.setAttribute('href', `books/${bookData['book']}`)
    bookPrice.innerText = `Купить ${bookData['book__price']}₽`

    previewContainer.style.cssText = `background-image: url(${imgUrl}); background-size: contain`
    bookTitle.innerText = bookData['book__name']
  }
  typingForm.appendChild(htmlTag)
  textBlock = typingForm.firstElementChild
  tags = [...textBlock.children]
  caretPosition = 0
  tag = tags[caretPosition]
  marginEnd = parseFloat(window.getComputedStyle(textBlock).marginBlockEnd)
}

if (
  localStorage.getItem('color-theme') === 'dark'
  || (
    !('color-theme' in localStorage)
    && window.matchMedia('(prefers-color-scheme: dark)').matches
  )
) {
  document.documentElement.classList.add('dark')
  toggleLight.classList.remove('hidden')
} else {
  document.documentElement.classList.remove('dark')
  toggleDark.classList.remove('hidden')
}

themeBtn.addEventListener('click', function () {

  toggleDark.classList.toggle('hidden')
  toggleLight.classList.toggle('hidden')

  if (localStorage.getItem('color-theme')) {
    if (localStorage.getItem('color-theme') === 'light') {
      document.documentElement.classList.add('dark')
      localStorage.setItem('color-theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('color-theme', 'light')
    }

  } else {
    if (document.documentElement.classList.contains('dark')) {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('color-theme', 'light')
    } else {
      document.documentElement.classList.add('dark')
      localStorage.setItem('color-theme', 'dark')
    }
  }

})
