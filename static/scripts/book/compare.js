function getSymbols(code) {
  return keycaps.get(code).symbols || null
}

typingForm.addEventListener('keydown', function (e) {
  if (!['Alt', 'Shift', 'Control', 'CapsLock'].includes(e.key)) {
    const tagContent = tag.textContent
    const symbols = getSymbols(e.code)
    if ((e.key.toLowerCase().match(/[a-zа-я]/) && e.key === tagContent)
      || (symbols && symbols.includes(tagContent))) {
      Object.assign(tag, {
        className: 'text-gray-300 dark:text-gray-500',
        style: 'background: transparent'
      })
      caretPosition++
      if (tag.lastChild.nodeName === 'BR') {
        newLine()
      } else if ((tagContent.charCodeAt(0) === 182 || tagContent === '\n')
        && e.code === 'Enter') {
        newLine(true)
      }
    } else {
      tag.style.cssText = 'background: orange; color: white;'
    }
    tag = tags[caretPosition]
    setCursorPosition(caretPosition)
  }
  getKey(e.code) && getKey(e.code).setAttribute('data-pressed', 'on')
  e.preventDefault()
})

// typingForm.addEventListener('keyup', function (e) {
//   const button = getKey(e.code)
//   if (button) {
//     const classes = button.classList
//
//     if (classes.contains('caps-active')) {
//       classes.remove('caps-active')
//     } else if (classes.contains('caps')) {
//       classes.add('caps-active')
//     }
//
//     button.removeAttribute('data-pressed')
//   }
// })