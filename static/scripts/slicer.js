function slicer(text) {
  let tags = []
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '\n') {
      tags.push(`<span>${text[i - 1] !== '-' ? ' ' : ''}<br></span>`)
    } else {
      tags.push(`<span>${text[i]}</span>`)
    }
  }
  tags.push('<span>&para;</span>')
  return tags.join('')
}