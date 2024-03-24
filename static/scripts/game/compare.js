document.addEventListener('DOMContentLoaded', function () {
  const height = window.getComputedStyle(tag).lineHeight
  document.getElementById('container').style.height = `${parseFloat(height) * 2}px`
})

let is_start = true
let isCorrect = true
let word_len = 0

textContainer.addEventListener('keydown', function (e) {
  if (!['Alt', 'Shift', 'Control', 'CapsLock', 'Delete'].includes(e.key)) {
    if (is_start) {
      timer()
      is_start = false
    }
    const tagContent = tag.textContent

    if (e.key.match(/[а-я -]/) && e.key === tagContent) {
      tag.style.cssText = 'background: transparent; color: lightgrey'
      word_len++
      if (e.code === 'Space') {
        score.value = parseInt(score.value) + word_len
        word_len = 0
        isCorrect && correctWords.value++
        wordCount.value++
        isCorrect = true
      }
      if (tag.lastChild.nodeName === 'BR') {
        newLine()
      }
      caretPosition++
    } else {
      parseInt(score.value) && score.value--
      tag.style.cssText = 'background: orange; color: white'
      isCorrect = false
    }
  }
  tag = tags[caretPosition]
  setCursorPosition(caretPosition)
  e.preventDefault()
})

function timer(seconds = 30) {
  TIMER.textContent = seconds
  const timer = setInterval(() => {
    if (seconds) {
      TIMER.textContent = seconds
      seconds--
    } else {
      clearInterval(timer)
      form.submit()
    }
  }, 1000)
}