from openai import OpenAI
import json

client = OpenAI()


def risk_agent_llm(income: float, debt: float, external_context: any = None):
    # convert external context to readable string, or show "No external data available" if empty
    context_str = json.dumps(external_context, indent=2) if external_context else "No external data available."

    prompt = f"""
You are a senior financial risk analyst at RBC.

Analyze the following loan applicant using both self-reported and verified bank data:

[Self-Reported Data]
- Annual Income: ${income}
- Total Debt: ${debt}

[Verified Bank Context (via MCP)]
{context_str}

Return ONLY a valid JSON object.

Strict rules:
- Weigh the "Verified Bank Context" higher than self-reported data.
- If history shows "Default", the risk_score should be significantly higher.
- Output must be parseable by json.loads().

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
        ],
        response_format={ "type": "json_object" } # json
    )

    content = response.choices[0].message.content
    print("LLM raw output:", content)
    
    try:
        result = json.loads(content)
    except Exception as e:
        # error handling
        result = {
            "risk_score": 0.9,
            "risk_level": "HIGH",
            "explanation": f"Error parsing LLM response: {str(e)}"
        }

    return result