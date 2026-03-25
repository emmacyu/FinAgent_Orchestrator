import json
from backend.utils.llm_client import call_llm


def fraud_agent_llm(income: float, debt: float, risk_score: float):
    prompt = f"""
You are a fraud detection expert.

Analyze whether this applicant shows signs of fraud.

Input:
Income: {income}
Debt: {debt}
Risk Score: {risk_score}

Return ONLY JSON:

{{
  "fraud_flag": true | false,
  "reason": "short explanation"
}}
"""

    response = call_llm(prompt)
    content = response["choices"][0]["message"]["content"]

    # 复用你已有的安全 parser（推荐）
    import re

    content = re.sub(r"```json|```", "", content).strip()
    json_str = re.search(r"\{.*\}", content, re.DOTALL).group()

    return json.loads(json_str)