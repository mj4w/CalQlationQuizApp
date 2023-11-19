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
        question: "	Evaluate lim┬(h → 0)⁡ (6 + h)^2 -36/h if it exists",
        choice1: "12",
        choice2: "3",
        choice3: "9",
        answer: 1,
    },
    {
        question: "	Evaluate lim┬(x → -3)⁡ √(2x + 22 - 4)/x + 3 if it exists",
        choice1: "1/4",
        choice2: "1/2",
        choice3: "1/3",
        answer: 1,
    },
    {
        question: "Determine where the following function is discontinuous. R(t) =  8t/(t^2  - 9t - 1)",
        choice1: "Function will be discontinuous at the points: t =  (4 ± √65)/3  ",
        choice2: "Function will be discontinuous at the points: t =  (9 ± √85)/2",
        choice3: "Function will be discontinuous at the points: t =  (4 ± √8)/3 ",
        answer: 2,
    },
    {
        question:"Find the derivative of Q(t) = 10 + 5t - t^2",
        choice1: "Q'(t) = 5 - 5t",
        choice2: "Q'(t) = 2 - t",
        choice3: "Q'(t) = 5 - 2t",
        answer: 3,
    },
    {
        question:"If f(x) = x^3 g(x),g(-7)= 2,g'(-7) = -9  determine the value of f'(7)",
        choice1: "3381",
        choice2: "2997",
        choice3: "3380",
        answer: 1,
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