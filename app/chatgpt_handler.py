import json
import os

import openai

from .services import BookingService


class ChatGPTService:
    openai.api_key = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def process_command(command: str):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for booking technicians. Provide structured JSON responses.",
                },
                {"role": "user", "content": command},
            ],
        )
        reply = response["choices"][0]["message"]["content"].strip()

        try:
            structured_response = json.loads(reply)  # ✅ Safe JSON Parsing
            name = structured_response.get("name")
            profession = structured_response.get("profession")
            date = structured_response.get("date")
            time = structured_response.get("time")

            if not all([name, profession, date, time]):
                raise ValueError("Missing required fields in response.")

            booking = BookingService.create_booking(name, profession, date, time)
            return {"message": "Booking confirmed", "booking": booking}
        except Exception as e:
            return {"error": f"Failed to process booking: {str(e)}"}
