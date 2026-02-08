# AI Interview Simulator (Backend)

An AI-powered technical interview simulator built using **FastAPI** and **Large Language Models (LLMs)**.  
This backend simulates a real technical interview experience by dynamically generating questions, evaluating answers, tracking performance, and producing an interview summary.

---

## 🚀 Features

- AI-generated interview questions
- Supports multiple interview types (DSA, Backend, etc.)
- Real-time answer evaluation with score and feedback
- Session-based interview tracking per user
- Final interview summary with strengths, weaknesses, and verdict
- REST API with Swagger documentation

---

## 🛠 Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- LLM-based evaluation & generation

---

## 📁 Project Structure

ai-interview-simulator/
│
├── Backend/
│ ├── main.py # FastAPI routes & session handling
│ ├── ai_engine.py # AI question generation & evaluation logic
│ ├── list_models.py # Available AI models
│
├── requirements.txt
├── .gitignore
└── README.md


---

## 📌 API Endpoints

### Get Question
POST /get-question

Generates the next interview question for the user.

### Submit Answer
POST /submit-answer

Evaluates the submitted answer and returns a score and feedback.

### End Interview
POST /end-interview

Returns a complete interview summary including average score and verdict.

---

## ▶️ Run Locally

```bash
cd Backend
pip install -r requirements.txt
uvicorn main:app --reload

Open:
http://127.0.0.1:8000/docs

🧠 How It Works

User starts an interview session

AI generates interview questions dynamically

User submits answers

AI evaluates answers and assigns scores

Performance is tracked per session

A final interview summary is generated

🔮 Future Improvements

Frontend UI (React / Next.js)

Voice-based interview (speech-to-text & text-to-speech)

AI interviewer avatar

Difficulty progression

Database persistence

Authentication

👤 Author

Pratik Chakraborty
Backend Developer | Python | FastAPI | AI Systems
