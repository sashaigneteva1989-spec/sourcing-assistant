from openai import OpenAI

from config import MODEL, GEMINI_API_KEY


client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def load_prompt():
    with open("prompts/hh_prompt.txt", encoding="utf-8") as f:
        return f.read()


def analyze_vacancy(text, model=MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": load_prompt()
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception:
        raise Exception(
            "Не удалось получить ответ от Gemini. Попробуйте еще раз через несколько секунд."
        )
