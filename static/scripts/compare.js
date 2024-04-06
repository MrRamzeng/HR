document.addEventListener('DOMContentLoaded', function () {
  init()
})

function newLine(end = false) {
  shift += parseFloat(window.getComputedStyle(tag).lineHeight)
  textContainer.style.cssText = `
    transition: top 0.2s linear; top: -${shift + (end ? marginEnd : 0)}px;
  `
  if (end) {
    textContainer.firstElementChild.remove()
    textContainer.style.cssText = 'transition: none; top: 0;'
    init()
  }
}