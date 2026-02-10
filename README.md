# AI Interview Simulator

An AI-powered technical interview simulator built with FastAPI and Large Language Models (LLMs).  
It dynamically generates interview questions, evaluates candidate answers, and produces an interview summary with strengths, weaknesses, and an overall verdict.

---

## 🚀 Features

- Dynamic interview question generation using LLMs
- Supports multiple interview types (DSA, Backend, etc.)
- Answer evaluation with scores and feedback
- Session-based interview tracking per user
- Final interview summary with strengths, weaknesses, and verdict
- REST APIs documented using Swagger (OpenAPI)

---

## 🛠 Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- LLM-based question generation and evaluation
- Git & GitHub

---

## 📂 Project Structure

ai-interview-simulator/
│
├── Backend/
│   ├── main.py            # FastAPI app and API routes
│   ├── ai_engine.py       # AI question generation & evaluation logic
│   ├── list_models.py     # Available AI models
│
├── requirements.txt
├── .gitignore
└── README.md

---

## 🔁 Interview Flow

1. User starts an interview session
2. AI generates an interview question
3. User submits an answer
4. AI evaluates the answer and assigns a score
5. Steps 2–4 repeat for multiple questions
6. Interview ends with a final performance summary

---

## ▶️ Run Locally

git clone https://github.com/<your-username>/ai-interview-simulator.git  
cd ai-interview-simulator  

pip install -r requirements.txt  

uvicorn Backend.main:app --reload  

Open Swagger UI at:  
http://127.0.0.1:8000/docs

---

## 📌 Future Improvements

- Frontend UI (React / Next.js)
- Voice-based interview (speech-to-text & text-to-speech)
- AI interviewer avatar
- Difficulty-level adaptation
- Persistent database storage
- User authentication and profiles

---

## 👤 Author

Pratik Chakraborty  
AI Interview Simulator Project
