from fastapi import FastAPI
from pydantic import BaseModel
import random
from ai_engine import configure_gemini, evaluate_answer, generate_question

def deduplicate_preserve_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


app = FastAPI()
# Temporary in-memory interview state (no DB)
interview_sessions = {}

# Configure Gemini once at startup
configure_gemini()
from ai_engine import warm_up_model
warm_up_model()

# -----------------------------
# Data models
# -----------------------------

class InterviewRequest(BaseModel):
    user_id: str
    interview_type: str


class EvaluationRequest(BaseModel):
    user_id: str
    question: str
    answer: str


# -----------------------------
# Sample questions
# -----------------------------

QUESTIONS = {
    "dsa": [
        "What is the difference between an array and a linked list?",
        "Explain how hash maps work and their time complexity."
    ],
    "hr": [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?"
    ]
}


# -----------------------------
# APIs
# -----------------------------

@app.post("/get-question")
def get_question(req: InterviewRequest):
    user_id = req.user_id
    interview_type = req.interview_type

    if user_id not in interview_sessions:
        interview_sessions[user_id] = {
            "interview_type": interview_type,
            "current_question": 1,
            "answers": [],
            "questions": []
        }

    session = interview_sessions[user_id]
    q_no = session["current_question"]
    previous_questions = session["questions"]

    question = generate_question(interview_type, q_no, previous_questions)
    session["questions"].append(question)
    session["current_question"] += 1

    return {
        "question_number": q_no,
        "question": question
    }




@app.post("/evaluate")
def evaluate(request: EvaluationRequest):
    ai_response = evaluate_answer(
        question=request.question,
        answer=request.answer
    )

    return {"evaluation": ai_response}


@app.post("/submit-answer")
def submit_answer(req: EvaluationRequest):
    user_id = req.user_id

    if user_id not in interview_sessions:
        return {"error": "Interview session not found"}

    evaluation = evaluate_answer(req.question, req.answer)

    interview_sessions[user_id]["answers"].append({
        "question": req.question,
        "answer": req.answer,
        "score": evaluation["score"],
        "feedback": evaluation["feedback"]
    })

    return {
        "message": "Answer recorded",
        "evaluation": evaluation
    }


@app.post("/end-interview")
def end_interview(user_id: str):
    if user_id not in interview_sessions:
        return {"error": "Interview session not found"}

    session = interview_sessions[user_id]
    answers = session["answers"]
    if len(answers) < 2:
        return {
            "total_questions": len(answers),
            "average_score": None,
            "strengths": [],
            "weaknesses": [],
            "verdict": "Not enough data to evaluate. Please answer more questions."
        }

    if not answers:
        return {"error": "No answers submitted"}

    total_questions = len(answers)
    scores = [a["score"] for a in answers]
    avg_score = round(sum(scores) / total_questions, 2)

    strengths = []
    weaknesses = []

    for a in answers:
        if a["score"] >= 7:
            strengths.append(f"Good understanding of {a['question']}")
        elif a["score"] <= 4:
            weaknesses.append(f"Needs improvement in {a['question']}")

    for a in answers:
        if a["score"] >= 7:
            strengths.append(a["question"])
        else:
            weaknesses.append(a["question"])

    if avg_score >= 7:
        verdict = "Strong performance"
    elif avg_score >= 5:
        verdict = "Average performance"
    else:
        verdict = "Needs improvement"

    summary = {
        "total_questions": total_questions,
        "average_score": avg_score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "verdict": verdict
    }

    # Optional: clear session after interview ends
    del interview_sessions[user_id]

    strengths = deduplicate_preserve_order(strengths)
    weaknesses = deduplicate_preserve_order(weaknesses)

    return summary
