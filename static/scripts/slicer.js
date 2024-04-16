function slicer(text, end = '\n') {
  let tags = []
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '\r') {
      continue
    }
    if (text[i] === '\n') {
      const previous = text[i - 2]
      const sep = previous === '-' ? '' : ' '
      if (sep) {
        tags.push(`<symbol>${sep}<br></symbol>`)
      } else {
        tags[tags.length - 1] = `<symbol>${previous}<br></symbol>`
      }
    } else {
      tags.push(`<symbol>${text[i]}</symbol>`)
    }
  }
  tags.push(`<symbol>${end}</symbol>`)
  return tags.join('')
}