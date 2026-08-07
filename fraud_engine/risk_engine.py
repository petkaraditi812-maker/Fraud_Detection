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
    # -----------------------------
    # Trust Factors (Reduce Risk)
    # -----------------------------

    if row["otp_verified"] == 1:
        risk_score -= 15
        reasons.append("OTP Verified")

    if row["trusted_device"] == 1:
        risk_score -= 10
        reasons.append("Trusted Device")

    if row["trusted_beneficiary"] == 1:
        risk_score -= 15
        reasons.append("Trusted Beneficiary")

    risk_score = max(risk_score, 0)


    fraud_flag = "Yes" if risk_score >= 50 else "No"

    if risk_score < 40:
        risk_level = "Low"
        fraud_flag = "No"
        action = "Approve"

    elif risk_score < 70:
        risk_level = "Medium"
        fraud_flag = "No"
        action = "Additional Verification"

    else:
        risk_level = "High"
        fraud_flag = "Yes"
        action = "Block Transaction"

    return risk_score, fraud_flag, risk_level, action, ", ".join(reasons)