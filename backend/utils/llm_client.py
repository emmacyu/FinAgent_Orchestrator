from openai import OpenAI

client = OpenAI()


def call_llm(prompt: str, model: str = "gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response