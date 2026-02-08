import os
import json
import ai_engine
from google import genai


def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)
    return client


client = configure_gemini()


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
            model="models/gemma-3-12b-it",
            contents=prompt
        )

        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        return json.loads(raw)

    except Exception as e:
        return {
            "score": 0,
            "feedback": f"AI failed safely: {str(e)}",
            "ideal_answer": ""
        }
def generate_question(interview_type: str, question_no: int, previous_questions: list):
    asked = "\n".join(f"- {q}" for q in previous_questions)

    prompt = f"""
    You are an interviewer conducting a {interview_type.upper()} technical interview.

    Previously asked questions:
    {asked if asked else "None"}

    Rules:
    - Do NOT repeat or rephrase any previous question
    - Ask a NEW question testing a different concept
    - Increase difficulty gradually
    - Avoid generic or common interview questions

    Ask question number {question_no}.

    Return ONLY the question text.
    """


    try:
        response = client.models.generate_content(
            model="models/gemma-3-12b-it",
            contents=prompt,
            generation_config={
                "temperature": 0.8
            }
        )
        return response.candidates[0].content.parts[0].text.strip()


    except Exception:
        try:
            response = client.models.generate_content(
                model="models/gemma-3-12b-it",
                contents=prompt
            )
            return response.text.strip()
        except Exception:
            return "Unable to generate question at the moment."
     

def warm_up_model():
    try:
        client.models.generate_content(
            model="models/gemma-3-12b-it",
            contents="Say hello"
        )
    except Exception:
        pass
