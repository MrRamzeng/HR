TIMER.textContent = timerField.options[timerField.selectedIndex].textContent

let is_start = true
let errors = 0

let symbols = 0

function setTimer() {
  TIMER.textContent = timerField.options[timerField.selectedIndex].textContent
}

const modeField = document.getElementById('id_mode')

let htmlTag = document.createElement('symbols')
textContainer.appendChild(htmlTag)

function getRandomNumber() {
  const multipliers = [
    10, 100, 1000, 10000, 100000, 1000000, -10, -100, -1000, -10000, -100000, -1000000,
  ]
  return (
    Math.random() * getRandomElement(multipliers)
  ).toFixed(2)
}

const getRandomElement = (arr) => {
  return arr[Math.floor(Math.random() * arr.length)]
}

const mix = (type1, type2) => {
  const probability = Math.random()
  return probability < 0.5 ? type1 : type2
}

const getContentType = (type) => {
  if (type === 'Только числа') {
    return getRandomNumber()
  } else if (type === 'Только знаки') {
    return getRandomElement(signs)
  } else if (type === 'Все') {
    const data = mix(getRandomElement(words), getRandomNumber())
    return mix(getRandomElement(signs), data)
  } else {
    return getRandomElement(words)
  }
}

function setContent(type) {
  let stringLen = 0
  let content = ''
  while (content.length < 3000) {
    const data = getContentType(type)
    const dataLen = data.length + 1
    if (stringLen + dataLen < 80) {
      content += `${data} `
      stringLen += dataLen
    } else {
      content += `${data}\n`
      stringLen = 0
    }
  }
  htmlTag.innerHTML = slicer(content)
  init()
}

textContainer.addEventListener('keydown', function (e) {
  if (!['Alt', 'Shift', 'Control', 'CapsLock', 'Delete'].includes(e.key)) {
    if (is_start) {
      timer(timerField.value)
      is_start = false
    }
    const tagContent = tag.textContent
    console.log(e.key, tagContent)
    if (e.key === tagContent) {
      tag.style.cssText = 'background: transparent; color: lightgrey'
      score.value++
      symbols++
      tag.lastChild.nodeName === 'BR' && newLine()
      caretPosition++
    } else {
      parseInt(score.value) && score.value--
      errors++
      tag.style.cssText = 'background: orange; color: white'
    }
    accuracy.value = ((symbols - errors) * 100 / (symbols || 1)).toFixed(2)
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
    if (timeStamp > 0) {
      timeStamp--
      let minutes = Math.floor(timeStamp / 60)
      let seconds = timeStamp % 60
      TIMER.textContent = `${minutes}:${seconds > 9 ? parseInt(seconds) : '0' + parseInt(seconds)}`
    } else {
      clearInterval(timer)
      speed.value = Math.floor(symbols / parseInt(timerField.value) * 60)
      form.submit()
    }
  }, 1000)
}