from openai import OpenAI
import json

client = OpenAI()

def risk_agent_llm(income: float, debt: float):
    prompt = f"""
You are a financial risk analyst.

Analyze the following loan applicant:

Income: {income}
Debt: {debt}

Return ONLY a valid JSON object.

Strict rules:
- Do NOT include any explanation outside JSON
- Do NOT include markdown (no ``` or ```json)
- Do NOT include any extra text
- Output must be parseable by json.loads()

The JSON must follow this exact schema:

{{
  "risk_score": float,        // between 0 and 1
  "risk_level": "LOW" | "MEDIUM" | "HIGH",
  "explanation": string
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    print("LLM raw output:", content)
    # 解析 JSON（实际工程中要加容错）
    result = json.loads(content)

    return result