def decision_agent(state: dict):
    risk_level = state.get("risk_level")

    if risk_level == "LOW":
        decision = "APPROVE"
    elif risk_level == "MEDIUM":
        decision = "REVIEW"
    else:
        decision = "REJECT"

    state["decision"] = decision
    return state