def calculate_risk(row):
    risk_score = 0
    reasons = []

    if row["amount"] > 50000:
        risk_score += 35
        reasons.append("High transaction amount")

    if row["amount_deviation"] > 30000:
        risk_score += 25
        reasons.append("Unusual spending compared to customer average")

    if row["is_night_tx"] == 1:
        risk_score += 10
        reasons.append("Night transaction")

    if row["tx_within_10min"] == 1:
        risk_score += 15
        reasons.append("Multiple transactions within 10 minutes")

    if row["location_changed"] == 1:
        risk_score += 10
        reasons.append("Location changed")

    if row["device_changed"] == 1:
        risk_score += 10
        reasons.append("Device changed")

    fraud_flag = "Yes" if risk_score >= 50 else "No"

    if risk_score >= 70:
        risk_level = "High"
    elif risk_score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return risk_score, fraud_flag, risk_level, ", ".join(reasons)