const pwd = document.getElementById("password1");
const pwd2 = document.getElementById("password2")
const letter = document.getElementById("letter");
const capital = document.getElementById("capital");
const number = document.getElementById("number");
const len = document.getElementById("length");

pwd.onkeyup = function () {
  const lowerCaseLetters = /[a-zа-я]/g;
  const upperCaseLetters = /[A-ZА-Я]/g;
  const numbers = /[0-9]/g;

  if (pwd.value.match(lowerCaseLetters)) {
    letter.classList.add("hidden");
  } else {
    letter.classList.remove("hidden");
  }

  if (pwd.value.match(upperCaseLetters)) {
    capital.classList.add("hidden");
  } else {
    capital.classList.remove("hidden");
  }

  if (pwd.value.match(numbers)) {
    number.classList.add("hidden");
  } else {
    number.classList.remove("hidden");
  }

  if (pwd.value.length >= 8) {
    len.classList.add("hidden");
  } else {
    len.classList.remove("hidden");
  }

  if (pwd.value.match(/^\S{8,}$/g)) {
    pwd.removeAttribute('class')
    pwd.classList.add(
      'block', 'w-full', 'p-2.5', 'bg-green-50', 'border', 'border-green-500', 'rounded-lg',
      'sm:text-sm', 'text-green-900', 'placeholder-green-700', 'focus:border-green-500',
      'focus:ring-green-500', 'dark:bg-gray-700', 'dark:border-green-500',
      'dark:text-green-400', 'dark:placeholder-green-500'
    )
  } else {
    pwd.removeAttribute('class')
    pwd.classList.add(
      'block', 'w-full', 'p-2.5', 'bg-red-50', 'border', 'border-red-500', 'rounded-lg',
      'sm:text-sm', 'text-red-900', 'placeholder-red-700', 'focus:border-red-500',
      'focus:ring-red-500', 'dark:bg-gray-700', 'dark:border-red-500', 'dark:text-red-500',
      'dark:placeholder-red-500'
    )
  }
}

pwd2.onkeyup = function () {
  if (pwd.value === pwd2.value) {
    pwd2.removeAttribute('class')
    pwd2.classList.add(
      'block', 'w-full', 'p-2.5', 'bg-green-50', 'border', 'border-green-500', 'rounded-lg',
      'sm:text-sm', 'text-green-900', 'placeholder-green-700', 'focus:border-green-500',
      'focus:ring-green-500', 'dark:bg-gray-700', 'dark:border-green-500',
      'dark:text-green-400', 'dark:placeholder-green-500'
    )
  } else {
    pwd2.removeAttribute('class')
    pwd2.classList.add(
      'block', 'w-full', 'p-2.5', 'bg-red-50', 'border', 'border-red-500', 'rounded-lg',
      'sm:text-sm', 'text-red-900', 'placeholder-red-700', 'focus:border-red-500',
      'focus:ring-red-500', 'dark:bg-gray-700', 'dark:border-red-500', 'dark:text-red-500',
      'dark:placeholder-red-500'
    )
  }
}