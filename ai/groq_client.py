import os
import json
import groq


class GroqClient:
    MODEL = "llama-3.1-8b-instant"

    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

    def summarise(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarise this text concisely in 2-3 sentences:\n\n{text}",
                }
            ],
        )
        return response.choices[0].message.content.strip()

    def chat(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
        )
        return response.choices[0].message.content.strip()

    def sentiment(self, text: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a sentiment analysis engine. "
                        'Respond ONLY with valid JSON in this exact format: '
                        '{"sentiment": "positive|negative|neutral", '
                        '"score": <float 0.0-1.0>, '
                        '"explanation": "<brief explanation>"}'
                    ),
                },
                {"role": "user", "content": text},
            ],
        )
        raw = response.choices[0].message.content.strip()
        return json.loads(raw)


def get_groq_client() -> GroqClient:
    return GroqClient()
