const textContainer = document.getElementById('text-container')
const bookInfo = document.getElementById('book-info')
const textPosition = document.getElementById('id_position')
const form = document.getElementById('text-form')
const score = document.getElementById('id_score')
const wordCount = document.getElementById('id_word_count')
const correctWords = document.getElementById('id_correct_words')
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
