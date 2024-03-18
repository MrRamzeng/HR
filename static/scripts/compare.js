document.addEventListener('DOMContentLoaded', function () {
  init()

  const getKey = (code) => {
    return document.querySelector(`[data-code="${code}"]`)
  }

  function getSymbols(code) {
    return keycaps.get(code).symbols || null
  }

  function newLine(end = false) {
    caretPosition++
    shift += parseFloat(window.getComputedStyle(tag).lineHeight)
    textContainer.style.cssText = `
        transition: top 0.3s linear; top: -${shift + (end ? marginEnd : 0)}px;
      `
    if (end) {
      textContainer.firstElementChild.remove()
      textContainer.style.cssText = 'transition: none; top: 0;'
      init()
    }
  }

  const newTextBlock = () => {
    textPosition && textPosition.value++
    newLine(true)
    bookInfo && bookInfo.firstElementChild.remove()
    form ? form.submit() : null
  }

  textContainer.addEventListener('keydown', function (e) {
    if (!['Alt', 'Shift', 'Control', 'CapsLock'].includes(e.key)) {
      const tagContent = tag.textContent
      const symbols = getSymbols(e.code)

      if ((e.key.toLowerCase().match(/[a-zа-я]/) && e.key === tagContent)
        || (symbols && symbols.includes(tagContent))) {
        tag.style.cssText = 'background: transparent; color: lightgrey;'
        if (tag.lastChild.nodeName === 'BR') {
          newLine()
        } else if ((tagContent.charCodeAt(0) === 182 || tagContent === '\n')
          && e.code === 'Enter') {
          newTextBlock()
        } else {
          caretPosition++
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

  textContainer.addEventListener('keyup', function (e) {
    const button = getKey(e.code)
    if (button) {
      const classes = button.classList

      if (classes.contains('caps-active')) {
        classes.remove('caps-active')
      } else if (classes.contains('caps')) {
        classes.add('caps-active')
      }

      button.removeAttribute('data-pressed')
    }
  })
})