let currentQuestion = 0; // Start with the first question
let userAnswers = {}; // Object to store user answers
const practiceModeInstanceId = document.getElementById('practiceModeInstanceId').value; // Get practice mode instance ID
function prevQuestion() {
  if (currentQuestion > 0) {
    showQuestion(currentQuestion - 1);
  }
}

function nextQuestion() {
  const totalQuestions = document.querySelectorAll('.question-container').length;
  if (currentQuestion < totalQuestions - 1) {
    showQuestion(currentQuestion + 1);
  } else {
    // If on the last question, handle submit logic here
    submitQuiz();
  }
}

function submitQuiz() {
  // Collect user answers and handle submission logic here

  const questions = document.querySelectorAll('.question-container');
  questions.forEach((question) => {
    const questionId = question.dataset.questionId;
    const selectedChoice = question.querySelector('input[type="radio"]:checked');
    if (selectedChoice) {
      userAnswers[questionId] = selectedChoice.value;
    } else {
      // If no choice is selected, mark the question as unanswered
      userAnswers[questionId] = 'unanswered';
    }
  });
  

  // Log user answers to console
  console.log('User Answers:', userAnswers);
  console.log('Practice Answers:', practiceModeInstanceId);

  // Here you can make an AJAX request to submit user answers to the server
  // Example:
  fetch('/submit-group-answers/', {
    method: 'POST',
    body: JSON.stringify({
      user_answers:userAnswers,
      practice_mode_instance_id:practiceModeInstanceId
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Network response was not ok.');
  })
  .then(data => {
    // Handle response from the server
    window.location.href = `/result-practice/${practiceModeInstanceId}/`;
  })
  .catch(error => {
    console.error('Error submitting answers:', error);
  });

  // Display submission message to the user
  const resultDiv = document.getElementById('result');
  // resultDiv.innerHTML = 'Quiz submitted!'; // Example result message
}

function showQuestion(questionNumber) {
  const questions = document.querySelectorAll('.question-container');
  questions.forEach(question => question.style.display = 'none');
  questions[questionNumber].style.display = 'block';

  const prevButton = document.querySelector('#prevButton');
  const nextButton = document.querySelector('#nextButton');

  if (questionNumber === 0) {
    prevButton.style.display = 'none';
  } else {
    prevButton.style.display = 'inline-block';
  }

  if (questionNumber === questions.length - 1) {
    nextButton.innerHTML = 'Submit';
  } else {
    nextButton.innerHTML = 'Next';
    nextButton.style.display = 'inline-block'; // Ensure next button is visible for non-last questions
  }

  currentQuestion = questionNumber;

  // Automatically proceed to the next question once an answer is chosen
  const choices = questions[currentQuestion].querySelectorAll('.choices input[type="radio"]');
  choices.forEach(choice => {
    choice.addEventListener('change', () => {
      if (currentQuestion < questions.length - 1) {
        nextQuestion();
      }
    });
  });
}

// Initially show the first question
showQuestion(currentQuestion);

