let isStart = true
let errors = 0
let symbols = 0

function setPreset(id) {
  TIMER.textContent = document.querySelector(`label[for="${id}"]`).textContent
}

const modeField = document.querySelector('input[name="mode"]:checked').id

let htmlTag = document.createElement('symbols')
typingForm.appendChild(htmlTag)

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
  if (type === 'D') {
    return getRandomNumber()
  } else if (type === 'S') {
    return getRandomElement(signs)
  } else if (type === 'ALL') {
    const data = mix(getRandomElement(words), getRandomNumber())
    return mix(getRandomElement(signs), data)
  } else {
    return getRandomElement(words)
  }
}

function setContent(type) {
  let content = ''
  let stringLen = 0
  while (content.length < 1000) {
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

typingForm.addEventListener('keydown', (e) => {
  const key = getKey(e.code)
  if (!['Alt', 'Shift', 'Control', 'CapsLock', 'Delete'].includes(e.key)) {
    if (isStart) {
      timer(document.querySelector('input[name="timer"]:checked').value)
      isStart = false
    }
    const tagContent = tag.textContent
    if (e.key === tagContent) {
      Object.assign(tag, {
        className: 'text-gray-300 dark:text-gray-600',
        style: 'background: transparent'
      })
      score.value++
      symbols++
      caretPosition++
      tag.lastChild.nodeName === 'BR' && newLine()
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

  key && key.setAttribute('data-pressed', 'on')
  e.preventDefault()
})

function setAnonymResult(timer, mode, score, accuracy, speed) {
  localStorage.setItem('anonym_result', `${timer} ${mode} ${score} ${accuracy} ${speed}`)
}

function timer(timeStamp) {
  const timer = setInterval(() => {
    if (timeStamp) {
      timeStamp--
      let minutes = Math.floor(timeStamp / 60)
      let seconds = timeStamp % 60
      TIMER.textContent = `${minutes}:${seconds > 9 ? parseInt(seconds) : '0' + parseInt(seconds)}`
    } else {
      clearInterval(timer)
      const time = document.querySelector('input[name="timer"]:checked').value
      speed.value = Math.floor(symbols * 60 / parseInt(time)      )
      if (isAuth) {
        form.submit()
      } else {
        const mode = document.querySelector('input[name="mode"]:checked').value
        setAnonymResult(time, mode, score.value, accuracy.value, speed.value)
      }
    }
  }, 1000)
}