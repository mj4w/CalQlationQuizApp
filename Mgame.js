const question = document.querySelector('#question');
const choices = Array.from(document.querySelectorAll('.choice-text'));
const progressText = document.querySelector('#progressText');
const scoreText = document.querySelector('#score');
const progressBarFull = document.querySelector('#progressBarFull');

let currentQuestion = {}
let acceptingAnswers = true
let score = 0
let questionCounter = 0
let availableQuestions = []

let questions = [
    {
        question: "Find the inverse of f(x) = 6x+15",
        choice1: "f^(-1) (x) = 1/15(x - 6)",
        choice2: "f^(-1) (x) = 6(x - 15)",
        choice3: "f^(-1) (x) =  1/6(x - 15)",
        answer: 3,
    },
    {
        question: "	Find the inverse of R(x) = x^3+6",
        choice1: "R^(-1) (x) = ∛(x - 6)",
        choice2: "R^(-1) (x) = √(6&x - 3)",
        choice3: "R^(-1) (x) = ∛(x - 3)",
        answer: 1,
    },
    {
        question: "Find the derivative of the function g (x)=x^2",
        choice1: "g'(x) = 2x",
        choice2: "g'(x) = x",
        choice3: "g'(x) = -2x",
        answer: 1,
    },
    {
        question:"	Find the derivative of the function f(x) = 2x^3 - 1",
        choice1: "f'(x) = 2x ",
        choice2: "f'(x) = 6x^2",
        choice3: "f'(x) = 3x^2 ",
        answer: 2,
    },
    {
        question:"Find the derivative of this function W (z) = 4z^2-9z",
        choice1: "W'(z) = 4z - 3",
        choice2: "W'(z) = 2z - 3",
        choice3: "W'(z) = 8z - 9",
        answer: 3,
    },
]

const SCORE_POINTS = 20
const MAX_QUESTIONS = 5

startGame = () => {
    questionCounter = 0
    score = 0
    availableQuestions = [...questions]
    getNewQuestion()
}

getNewQuestion = () => {
    if(availableQuestions.length === 0 || questionCounter > MAX_QUESTIONS) {
        localStorage.setItem('mostRecentScore', score)

        return window.location.assign('/end.html')
    }

    questionCounter++
    progressText.innerText = `Question ${questionCounter} of ${MAX_QUESTIONS}`
    progressBarFull.style.width = `${(questionCounter/MAX_QUESTIONS) * 100}%`
    
    const questionsIndex = Math.floor(Math.random() * availableQuestions.length)
    currentQuestion = availableQuestions[questionsIndex]
    question.innerText = currentQuestion.question

    choices.forEach(choice => {
        const number = choice.dataset['number']
        choice.innerText = currentQuestion['choice' + number]
    })

    availableQuestions.splice(questionsIndex, 1)

    acceptingAnswers = true
}

choices.forEach(choice => {
    choice.addEventListener('click', e => {
        if(!acceptingAnswers) return

        acceptingAnswers = false
        const selectedChoice = e.target
        const selectedAnswer = selectedChoice.dataset['number']

        let classToApply = selectedAnswer == currentQuestion.answer ? 'correct' : 'incorrect'

        if(classToApply === 'correct') {
            incrementScore(SCORE_POINTS)
        }

        selectedChoice.parentElement.classList.add(classToApply)

        setTimeout(() => {
            selectedChoice.parentElement.classList.remove(classToApply)
            getNewQuestion()

        }, 1000)
    })
})

incrementScore = num => {
    score +=num
    scoreText.innerText = score
}

startGame()