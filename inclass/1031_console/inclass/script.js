// Questions array
const questions = [
  {
    question: "What is the capital of France?",
    options: ["Berlin", "Madrid", "Paris", "Lisbon"],
    answer: 2
  },
  {
    question: "Which language is used for web development?",
    options: ["Python", "JavaScript", "C++", "Java"],
    answer: 1
  },
  {
    question: "What does CSS stand for?",
    options: [
      "Creative Style Sheets",
      "Computer Style Sheets",
      "Cascading Style Sheets",
      "Colorful Style Sheets"
    ],
    answer: 2
  }
];

let currentQuestionIndex = 0;
let score = 0;

const questionElement = document.getElementById("question");
const optionsElements = document.querySelectorAll(".option");
const nextButton = document.getElementById("next-button");

// Add event listener for the next button
nextButton.addEventListener('click', nextQuestion);

function loadQuestion() {
  const currentQuestion = questions[currentQuestionIndex];
  questionElement.textContent = currentQuestion.question;

  optionsElements.forEach((button, index) => {
    button.textContent = currentQuestion.options[index];
    button.classList.remove("correct", "wrong");
    // Re-enable buttons for the next question
    button.style.pointerEvents = "auto";
  });

  nextButton.style.display = "none";
}

function selectAnswer(selectedIndex) {
  const correctIndex = questions[currentQuestionIndex].answer;

  optionsElements.forEach((button, index) => {
    // Disable all buttons after an answer is selected
    button.style.pointerEvents = "none";
    
    if (index === correctIndex) {
      button.classList.add("correct");
    } else if (index === selectedIndex) {
      button.classList.add("wrong");
    }
  });

  if (selectedIndex === correctIndex) {
    score++;
  }

  nextButton.style.display = "block";
}

function nextQuestion() {
  currentQuestionIndex++;
  if (currentQuestionIndex < questions.length) {
    loadQuestion();
  } else {
    showScore();
  }
}

function showScore() {
  questionElement.textContent = `You scored ${score} out of ${questions.length}!`;
  optionsElements.forEach(button => (button.style.display = "none"));
  nextButton.style.display = "none";
}

loadQuestion();