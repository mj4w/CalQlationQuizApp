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
        question: "y = (x^4 + 1)^1/2; y''",
        choice1: "y'' = 2x^2 (x^4+1)^-3/2(x^4+3)",
        choice2: "y'' = 2x^2 (x^4-1)^3/2(x^4-3)",
        choice3: "y'' = 2x^2 (x^4-1)^-3/2(x^4+2)",
        answer: 1,
    },
    {
        question: "lim_(x→0)[(sin 6x^2)/x^2 × 6/6]",
        choice1: "5",
        choice2: "4",
        choice3: "6",
        answer: 3,
    },
    {
        question: "First derivative of y = sin 5x",
        choice1: "5 cos 5x",
        choice2: "5 sin 5x",
        choice3: "cos 5x ",
        answer: 1,
    },
    {
        question:"Evaluate Arcsin (cos  π/4)",
        choice1: "y =sin 4",
        choice2: "y =  π/4",
        choice3: "y = cos  π/4",
        answer: 2,
    },
    {
        question:"Differentiate y = sin h 4",
        choice1: "y''= 4 sin h 4x",
        choice2: "y'= 4 cos h 4x ",
        choice3: "y'= cos h 4x",
        answer: 2,
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