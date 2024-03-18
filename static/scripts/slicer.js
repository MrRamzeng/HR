function slicer(text, end = '\n') {
  let tags = []
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '\n') {
      const previous = text[i - 1]
      const sep = previous === '-' ? '' : ' '
      if (sep) {
        tags.push(`<span>${sep}<br></span>`)
      } else {
        tags[i - 1] = `<span>${previous}<br></span>`
      }
    } else {
      tags.push(`<span>${text[i]}</span>`)
    }
  }
  tags.push(`<span>${end}</span>`)
  return tags.join('')
}