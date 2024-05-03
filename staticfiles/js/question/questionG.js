// Set the total time for the quiz in seconds
var totalTime = 10000; // 10 seconds for testing purposes

// Variable to store the remaining time
var timeRemaining = totalTime;

// Function to start the timer
function startTimer() {
  var timerBar = document.getElementById('timer-bar');

  // Calculate the width of the timer bar for each iteration
  var barIncrement = 100 / totalTime;

  // Update the timer every 100 milliseconds for a smoother animation
  var timerInterval = setInterval(function () {
    timeRemaining -= 0.1; // Decrease by 0.1 for smoother animation

    // Update the timer bar width
    var percentageRemaining = (timeRemaining / totalTime) * 100;
    var timerWidth = 100 - percentageRemaining; // Adjust to make the bar move from right to left
    timerBar.style.width = timerWidth + '%';

    // Check if the time is up
    if (timeRemaining <= 0) {
      clearInterval(timerInterval);

      // Redirect to another page after the timer ends
      window.location.href = '/group-students'; // Replace with the actual URL

      // You can also submit the quiz or perform other actions if needed
      // submitQuiz();
    }
  }, 100);
}

// Call the startTimer function when the page loads
startTimer();

