from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(
    question: str,
    summaries: list,        # ChatSummary objects
    recent_chats: list,     # ChatHistory objects
    context: str,
stream: bool = False
):

    history_text = ""

    # 🔹 Summarized memory (compressed)
    for s in summaries:
        history_text += f"""
Conversation summary:
{s.summary}
"""

    # 🔹 Recent raw turns (verbatim)
    for chat in recent_chats:
        history_text += f"""
User: {chat.question}
Assistant: {chat.answer}
"""

    prompt = f"""
You are an assistant answering questions based on an internal document.

Rules:
- If the document clearly contains information relevant to the question,
  answer using ONLY the facts present in the document.
- If the document does NOT contain relevant information,
  answer using general knowledge instead.
- In all cases, do NOT mention the document, internal sources,
  missing context, or limitations explicitly.
- You MAY explain clearly and professionally in your own words.
- Do NOT add speculative or false information.

Follow-up question rules (IMPORTANT):
- ALWAYS include exactly ONE follow-up question at the end of the response.
- The follow-up question MUST be directly derived from the explanation you just gave.
- The follow-up question MUST advance the discussion to a different detail, condition,
  exception, or related section mentioned in the document.
- Do NOT ask generic questions.

Conversation history:
{history_text}

Document:
{context}

Question:
{question}

Write a clear, professional answer.
"""
    if stream:
        with client.responses.stream(
                model="gpt-4o-mini",
                input=prompt,  # ✅ USE FULL PROMPT
                temperature=0.2,
        ) as stream_response:

            for event in stream_response:
                if event.type == "response.output_text.delta" and event.delta:
                    yield event.delta  # ✅ ALWAYS STRING

        return

        # 🔥 NORMAL MODE
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.2
    )

    return response.output_text.strip() if response.output_text else "No answer generated."
