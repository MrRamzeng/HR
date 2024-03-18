const textContainer = document.getElementById('text-container')
const bookInfo = document.getElementById('book-info')
const textPosition = document.getElementById('id_position')
const form = document.getElementById('text-form')
// const inp = document.getElementById('inp')

let textBlock, caretPosition, tag, shift, marginEnd

function init() {
  textBlock = textContainer.firstElementChild
  tags = [...textBlock.children]
  caretPosition = 0
  tag = tags[caretPosition]
  shift = 0
  marginEnd = parseFloat(window.getComputedStyle(textBlock).marginBlockEnd)
}
