// Quiz Logic
let currentQuestion = 0;
let score = 0;
const totalQuestions = 10;
const difficulty = sessionStorage.getItem("difficulty"); // Retrieve user's selected difficulty
const operation = sessionStorage.getItem("operation"); // Retrieve user's selected operation
const progressElement = document.getElementById("progress");
const questionElement = document.getElementById("question");
const formElement = document.getElementById("quiz-form");
const answerInput = document.getElementById("answer");

function generateRandomNumber(range) {
    switch (difficulty) {
        case "easy":
            return Math.floor(Math.random() * range) + 1; // 1 to `range`
        case "advance":
            return Math.floor(Math.random() * range) + 10; // 10 to `range + 10`
        case "expert":
            return Math.floor(Math.random() * range) + 100; // 100 to `range + 100`
        default:
            return Math.floor(Math.random() * range) + 1;
    }
}

function generateQuestion() {
    const num1 = generateRandomNumber(difficulty === "easy" ? 10 : difficulty === "advance" ? 90 : 900);
    const num2 = generateRandomNumber(difficulty === "easy" ? 10 : difficulty === "advance" ? 90 : 900);
    let questionText = "";
    let correctAnswer = 0;

    switch (operation) {
        case "addition":
            questionText = `${num1} + ${num2}`;
            correctAnswer = num1 + num2;
            break;
        case "subtraction":
            questionText = `${num1} - ${num2}`;
            correctAnswer = num1 - num2;
            break;
        case "multiplication":
            questionText = `${num1} × ${num2}`;
            correctAnswer = num1 * num2;
            break;
        case "division":
            // Ensure clean division
            const dividend = num1 * num2;
            questionText = `${dividend} ÷ ${num2}`;
            correctAnswer = dividend / num2;
            break;
    }

    return { questionText, correctAnswer };
}

function updateQuestion() {
    if (currentQuestion < totalQuestions) {
        const { questionText, correctAnswer } = generateQuestion();
        questionElement.textContent = questionText;
        questionElement.dataset.correctAnswer = correctAnswer; // Store the correct answer for validation
        progressElement.textContent = `Question: ${currentQuestion + 1}/${totalQuestions}`;
        answerInput.value = ""; // Clear input field
    } else {
        // Quiz finished
        sessionStorage.setItem("score", score); // Store the score
        window.location.href = "Results.html"; // Redirect to results page
    }
}

// Event Listener for Form Submission
formElement.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevent form submission/reload
    const userAnswer = parseFloat(answerInput.value);
    const correctAnswer = parseFloat(questionElement.dataset.correctAnswer);

    if (userAnswer === correctAnswer) {
        score++;
    }

    currentQuestion++;
    updateQuestion();
});

// Start Quiz
updateQuestion();