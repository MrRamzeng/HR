document.addEventListener('DOMContentLoaded', function () {
  const height = window.getComputedStyle(tag).lineHeight
  TIMER.textContent = timerField.options[timerField.selectedIndex].textContent
  document.getElementById('container').style.height = `${parseFloat(height) * 2}px`
})

let is_start = true
let errors = 0

function setTimer() {
  TIMER.textContent = timerField.options[timerField.selectedIndex].textContent
}

textContainer.addEventListener('keydown', function (e) {
  if (!['Alt', 'Shift', 'Control', 'CapsLock', 'Delete'].includes(e.key)) {
    if (is_start) {
      timer(timerField.value)
      is_start = false
    }
    const tagContent = tag.textContent

    if (e.key.match(/[а-я -]/) && e.key === tagContent) {
      tag.style.cssText = 'background: transparent; color: lightgrey'
      score.value++
      if (tag.lastChild.nodeName === 'BR') {
        newLine()
      }
      caretPosition++
    } else {
      parseInt(score.value) && score.value--
      errors++
      tag.style.cssText = 'background: orange; color: white'
    }
    accuracy.value = ((caretPosition - errors) * 100 / (caretPosition || 1)).toFixed(2)
    if (parseInt(accuracy.value) < 0) {
        accuracy.value = 0
    }
  }
  tag = tags[caretPosition]
  setCursorPosition(caretPosition)
  e.preventDefault()
})

function timer(timeStamp) {
  const timer = setInterval(() => {
    if (timeStamp) {
      timeStamp--
      let minutes = Math.floor(timeStamp / 60)
      let seconds = timeStamp % 60
      TIMER.textContent = `${minutes}:${seconds > 9 ? seconds : '0' + seconds}`
    } else {
      clearInterval(timer)
      speed.value = Math.floor(caretPosition / parseInt(timerField.value) * 60)
      form.submit()
    }
  }, 1000)
}