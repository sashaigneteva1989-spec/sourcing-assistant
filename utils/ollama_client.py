import ollama

MODEL = "qwen2.5:7b"


def load_prompt():
    with open("prompts/hh_prompt.txt", encoding="utf-8") as f:
        return f.read()


def analyze_vacancy(text):
    response = ollama.chat(
        model=MODEL,
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
        options={
            "temperature": 0.2,
            "num_predict": 600
        }
    )

    return response["message"]["content"]