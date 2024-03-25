const textContainer = document.getElementById('text-container')
const bookInfo = document.getElementById('book-info')
const textPosition = document.getElementById('id_position')
const form = document.getElementById('text-form')
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
