// ==============================
// Config
// ==============================
const API_BASE = "http://127.0.0.1:8000";
const USER_ID = "user1"; // static for now, fine for MVP

// ==============================
// DOM Elements
// ==============================
const interviewTypeSelect = document.getElementById("interviewTypeSelect");
const startBtn = document.getElementById("startInterviewBtn");
const voiceToggle = document.getElementById("voiceModeToggle");
const submitBtn = document.getElementById("submitAnswerBtn");
const nextBtn = document.getElementById("nextQuestionBtn");
const endBtn = document.getElementById("endInterviewBtn");

const questionBox = document.getElementById("questionBox");
const answerInput = document.getElementById("answerInput");
const recordBtn = document.getElementById("recordBtn");
const recordStatus = document.getElementById("recordStatus");
const resultBox = document.getElementById("summaryText");


// ==============================
// State
// ==============================
let currentQuestion = "";
let currentQuestionNumber = 0;

// ==============================
// Helpers
// ==============================
function setQuestion(text) {
  questionBox.innerText = text;
}

function clearAnswer() {
  answerInput.value = "";
}
// ==============================
// speak function
// ==============================

function setResult(text) {
  resultBox.innerText = text;
}
function speak(text) {
    if (!voiceToggle.checked) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;

    window.speechSynthesis.cancel(); // stop previous speech
    window.speechSynthesis.speak(utterance);
}
// ===============================
// Speech Recognition Setup
// ===============================

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
        let transcript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }

        answerInput.value = transcript;
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        recordStatus.textContent = "Error occurred.";
    };

    recognition.onend = () => {
        recordStatus.textContent = "";
        recordBtn.textContent = "🎙️ Start Recording";
    };
}
// ==============================
// API Calls
// ==============================
async function getQuestion() {
  const interviewType = interviewTypeSelect.value;

  setQuestion("Loading question...");

  try {
    const response = await fetch(`${API_BASE}/get-question`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: USER_ID,
        interview_type: interviewType
      })
    });

    const data = await response.json();

    currentQuestion = data.question;
    currentQuestionNumber = data.question_number;

    setQuestion(data.question);
    speak(data.question);
  } catch (error) {
    console.error(error);
    setQuestion("Server error. Is backend running?");
  }
}

async function submitAnswer() {
  const answer = answerInput.value.trim();

  if (!answer) {
    alert("Please write an answer first.");
    return;
  }

  try {
    await fetch(`${API_BASE}/submit-answer`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: USER_ID,
        question: currentQuestion,
        answer: answer
      })
    });

    alert("Answer submitted successfully.");
    clearAnswer();
  } catch (error) {
    console.error(error);
    alert("Failed to submit answer.");
  }
}

async function endInterview() {
  console.log("END INTERVIEW CLICKED");

  setResult("Generating interview summary...");

  try {
    const response = await fetch(
      `${API_BASE}/end-interview?user_id=${USER_ID}`,
      {
        method: "POST"
      }
    );

    const data = await response.json();
    console.log("END INTERVIEW RESPONSE:", data);

    let summaryText = "";
    summaryText += `Total Questions: ${data.total_questions}\n`;
    summaryText += `Average Score: ${data.average_score}\n\n`;

    summaryText += "Strengths:\n";
    if (data.strengths.length === 0) {
      summaryText += "- None\n";
    } else {
      data.strengths.forEach(q => {
        summaryText += `- ${q}\n`;
      });
    }

    summaryText += "\nWeaknesses:\n";
    if (data.weaknesses.length === 0) {
      summaryText += "- None\n";
    } else {
      data.weaknesses.forEach(q => {
        summaryText += `- ${q}\n`;
      });
    }

    summaryText += `\nVerdict: ${data.verdict}`;

    setResult(summaryText);
    setQuestion("Interview ended.");
  } catch (error) {
    console.error(error);
    setResult("Failed to generate summary.");
  }
}

// ==============================
// Event Listeners
// ==============================
startBtn.addEventListener("click", () => {
  getQuestion();
});

submitBtn.addEventListener("click", () => {
  submitAnswer();
});

nextBtn.addEventListener("click", () => {
  getQuestion();
});

endBtn.addEventListener("click", () => {
  endInterview();
});

recordBtn.addEventListener("click", () => {
    if (!recognition) {
        alert("Speech Recognition not supported in this browser.");
        return;
    }

    if (recordBtn.textContent.includes("Start")) {
        recognition.start();
        recordBtn.textContent = "🛑 Stop Recording";
        recordStatus.textContent = "Listening...";
    } else {
        recognition.stop();
        recordBtn.textContent = "🎙️ Start Recording";
        recordStatus.textContent = "";
    }
});
