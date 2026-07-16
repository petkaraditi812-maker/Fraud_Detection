from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import psycopg2
import csv
from django.http import HttpResponse

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="fraud_analytics",
        user="postgres",
        password="Aditi@123"
    )


@csrf_exempt
def detect_fraud(request):
    return JsonResponse({
        "message": "AI-Powered Fraud Detection API is working",
        "endpoints": {
            "realtime_check": "/api/realtime-check/",
            "fraud_transactions": "/api/fraud-transactions/",
            "dashboard_summary": "/api/dashboard-summary/"
        }
    })


@csrf_exempt
def realtime_fraud_check(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    amount = float(data.get("amount", 0))
    amount_deviation = float(data.get("amount_deviation", 0))
    is_night_tx = int(data.get("is_night_tx", 0))
    tx_within_10min = int(data.get("tx_within_10min", 0))
    location_changed = int(data.get("location_changed", 0))

    risk_score = 0
    reasons = []

    if amount > 50000:
        risk_score += 40
        reasons.append("High transaction amount")

    if amount_deviation > 30000:
        risk_score += 25
        reasons.append("Unusual amount compared to user average")

    if is_night_tx == 1:
        risk_score += 10
        reasons.append("Night transaction")

    if tx_within_10min == 1:
        risk_score += 15
        reasons.append("Multiple transactions within 10 minutes")

    if location_changed == 1:
        risk_score += 10
        reasons.append("Location changed")

    fraud_flag = "Yes" if risk_score >= 50 else "No"

    if risk_score >= 70:
        risk_level = "High"
    elif risk_score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return JsonResponse({
        "transaction_id": data.get("transaction_id"),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "fraud_flag": fraud_flag,
        "fraud_reasons": reasons
    })


def fraud_transactions(request):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        transaction_id,
        user_id,
        amount,
        risk_score,
        fraud_flag,
        fraud_reason,
        transaction_time,
        ml_prediction,
        city,
        state,
        merchant_name,
        merchant_category,
        payment_method,
        device,
        risk_level
    FROM fraud_transactions
    ORDER BY transaction_time DESC
    LIMIT 100
""")

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append({
    "transaction_id": row[0],
    "user_id": row[1],
    "amount": float(row[2]),
    "risk_score": row[3],
    "fraud_flag": row[4],
    "fraud_reason": row[5],
    "transaction_time": str(row[6]),
    "ml_prediction": row[7],
    "city": row[8],
    "state": row[9],
    "merchant_name": row[10],
    "merchant_category": row[11],
    "payment_method": row[12],
    "device": row[13],
    "risk_level": row[14]
})
    cursor.close()
    conn.close()

    return JsonResponse({"fraud_transactions": data})


def dashboard_summary(request):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM fraud_transactions")
    total_frauds = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(risk_score) FROM fraud_transactions")
    avg_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM fraud_transactions WHERE risk_score >= 70")
    high_risk = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM fraud_transactions")
    total_fraud_amount = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return JsonResponse({
        "total_fraud_transactions": total_frauds,
        "average_risk_score": round(float(avg_risk), 2) if avg_risk else 0,
        "high_risk_transactions": high_risk,
        "total_fraud_amount": float(total_fraud_amount) if total_fraud_amount else 0
    })

def export_fraud_csv(request):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
SELECT
transaction_id,
user_id,
amount,
risk_score,
fraud_flag,
fraud_reason,
transaction_time,
ml_prediction,
city,
state,
merchant_name,
merchant_category,
payment_method,
device,
risk_level
FROM fraud_transactions
ORDER BY transaction_time DESC
LIMIT 100
""")

    rows = cursor.fetchall()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="fraud_transactions.csv"'

    writer = csv.writer(response)

    writer.writerow([
    "transaction_id",
    "user_id",
    "amount",
    "risk_score",
    "fraud_flag",
    "fraud_reason",
    "transaction_time",
    "ml_prediction",
    "city",
    "state",
    "merchant_name",
    "merchant_category",
    "payment_method",
    "device",
    "risk_level"


    for row in rows:
        writer.writerow(row)

    cursor.close()
    conn.close()

    return response