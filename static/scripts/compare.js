document.addEventListener('DOMContentLoaded', function () {
  init()
})

function newLine(end = false) {
  const POS = caretPosition
  caretPosition = 0
  tags.splice(0, POS)
  // const shift = parseFloat(window.getComputedStyle(tag).lineHeight)
  // typingForm.style.cssText = `
  //   transition: top 0.1s linear; top: -${shift + (end ? marginEnd : 0)}px;
  // `

  // setTimeout(() => {
    for (let pos = 0; pos < POS; pos++) {
      textBlock.firstElementChild.remove()
    }
  //   typingForm.style.cssText = 'transition none; top: 0;'
    textBlock.style.textIndent = 0
  // }, 100);
  // textBlock.removeAttribute('class')

  if (end) {
    typingForm.firstElementChild.remove()
    init()
  }
}