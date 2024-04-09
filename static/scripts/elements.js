const textContainer = document.getElementById('text-container')
const bookInfo = document.getElementById('book-info')
const textPosition = document.getElementById('id_position')
const form = document.getElementById('text-form')
// theme
const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon')
const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon')
const themeToggleBtn = document.getElementById('theme-toggle')
// accuracy game
const score = document.getElementById('id_score')
const accuracy = document.getElementById('id_accuracy')
const speed = document.getElementById('id_speed')
const timerField = document.getElementById('id_timer')
const TIMER = document.getElementById('timer')

// const inp = document.getElementById('inp')

let textBlock, caretPosition, tags, tag, shift, marginEnd

function init() {
  textBlock = textContainer.firstElementChild
  tags = [...textBlock.children]
  caretPosition = 0
  tag = tags[caretPosition]
  shift = 0
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
  themeToggleLightIcon.classList.remove('hidden')
} else {
  document.documentElement.classList.remove('dark')
  themeToggleDarkIcon.classList.remove('hidden')
}

themeToggleBtn.addEventListener('click', function () {

  themeToggleDarkIcon.classList.toggle('hidden')
  themeToggleLightIcon.classList.toggle('hidden')

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
