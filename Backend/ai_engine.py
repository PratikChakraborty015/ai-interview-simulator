import os
import json
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

client = None


def configure_gemini():
    global client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")

    client = genai.Client(api_key=api_key)
    print(f"✓ Gemini configured successfully")
    return client


def evaluate_answer(question: str, answer: str):
    prompt = f"""
You are a strict technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Return ONLY valid JSON.
No markdown.
No explanations.

Format:
{{
  "score": 1-10,
  "feedback": "short feedback",
  "ideal_answer": "short ideal answer"
}}
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-3.5-flash",
            contents=prompt
        )

        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        return json.loads(raw)

    except Exception as e:
        print(f"ERROR evaluating answer: {str(e)}")
        return {
            "score": 0,
            "feedback": f"AI evaluation failed: {str(e)}",
            "ideal_answer": ""
        }
def generate_question(interview_type: str, question_no: int, previous_questions: list):
    asked = "\n".join(f"- {q}" for q in previous_questions)

    prompt = f"""
    You are an expert technical interviewer.

    Interview type: {interview_type}
    Question number: {question_no}

    Previously asked questions:
    {asked if asked.strip() else "None"}

    TASK:
    Generate ONE NEW interview question for the given interview type.

    STRICT RULES:
    - The question MUST match the interview type.
    - The question MUST be different from all previously asked questions.
    - DO NOT repeat or paraphrase previous questions.
    - DO NOT include numbering.
    - DO NOT include explanations.
    - Return ONLY the question text.

    If interview_type is:
    - DSA → ask Data Structures or Algorithms question
    - AI_ML → ask Machine Learning / AI question
    - CORE_CS → ask OS, DBMS, CN, or OOP question
    - HR → ask HR question
    - BEHAVIORAL → ask behavioral question
    """




    try:
        response = client.models.generate_content(
            model="models/gemini-3.5-flash",
            contents=prompt
        )
        return response.candidates[0].content.parts[0].text.strip()


    except Exception as e:
        print(f"ERROR generating question: {str(e)}")
        try:
            response = client.models.generate_content(
                model="models/gemini-3.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e2:
            print(f"ERROR (fallback failed): {str(e2)}")
            return "Unable to generate question at the moment."
     

def warm_up_model():
    try:
        client.models.generate_content(
            model="models/gemini-3.5-flash",
            contents="Say hello"
        )
    except Exception:
        pass
