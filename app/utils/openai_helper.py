import json
import os

import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are an AI assistant for a technician booking system.
Users can:
- Book a technician by providing a profession and date.
- Check all their bookings.
- Cancel a booking by providing a booking ID.

If a user says "tomorrow", return:
    - "date": "YYYY-MM-DD" (with tomorrow's actual date)

If a user provides a specific date, return:
    - "date": "YYYY-MM-DD"

If a user wants to book, extract:
    - "action": "book"
    - "profession": e.g., "Plumber", "Electrician", "Gardener"
    - "date": "YYYY-MM-DD"

If a user asks about their bookings, return:
    - "action": "check_booking"

If a user wants to cancel a booking, return:
    - "action": "cancel"
    - "booking_id": 123 (if provided)

Return structured JSON:
{
    "action": "book" | "check_booking" | "cancel",
    "profession": "Plumber",
    "date": "2025-03-06",
    "booking_id": 123
}
"""


def get_openai_response(prompt: str) -> dict:
    """Send the user input to OpenAI's GPT model and return a structured response."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "Missing OpenAI API Key. Set OPENAI_API_KEY as an environment variable."
        )

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    ai_text_response = response.choices[0].message.content.strip()

    try:
        ai_response = json.loads(ai_text_response)
    except json.JSONDecodeError:
        ai_response = {
            "action": "unknown",
            "message": "I'm sorry, I didn't understand that.",
        }

    return ai_response
