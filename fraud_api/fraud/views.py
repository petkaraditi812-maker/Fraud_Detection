from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import csv
import psycopg2
import pandas as pd

from fraud_engine.predict import predict_fraud


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="fraud_analytics",
        user="postgres",
        password="Aditi@123"
    )


# ================================
# API CHECK
# ================================

@csrf_exempt
def detect_fraud(request):

    return JsonResponse({
        "message": "AI-Powered Fraud Detection API is working",
        "endpoints": {
            "realtime_check": "/api/realtime-check/",
            "fraud_transactions": "/api/fraud-transactions/",
            "dashboard_summary": "/api/dashboard-summary/",
            "export_csv": "/api/export-csv/"
        }
    })


# ================================
# REAL TIME ML FRAUD DETECTION API
# ================================

@csrf_exempt
def realtime_fraud_check(request):

    print("REQUEST METHOD:", request.method)

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=400
        )


    try:
        data = json.loads(request.body)

    except Exception:

        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )


    try:

        transaction = {

            "amount": float(data.get("amount", 0)),

            "amount_deviation": float(
                data.get("amount_deviation", 0)
            ),

            "is_night_tx": int(
                data.get("is_night_tx", 0)
            ),

            "tx_within_10min": int(
                data.get("tx_within_10min", 0)
            ),

            "location_changed": int(
                data.get("location_changed", 0)
            ),

            "device_changed": int(
                data.get("device_changed", 0)
            ),

            "otp_verified": int(
                data.get("otp_verified", 1)
            ),

            "trusted_device": int(
                data.get("trusted_device", 1)
            ),

            "trusted_beneficiary": int(
                data.get("trusted_beneficiary", 1)
            )
        }


        df = pd.DataFrame([transaction])


        # ML Prediction

        result = predict_fraud(df)


        prediction = result.iloc[0]["ml_prediction"]


        probability = float(
            result.iloc[0]["fraud_probability"]
        )


        confidence = result.iloc[0]["prediction_confidence"]



        # Risk Level

        if probability >= 75:
            risk_level = "High"

        elif probability >= 50:
            risk_level = "Medium"

        else:
            risk_level = "Low"



        # Fraud Reasons

        reasons=[]


        if transaction["amount"] > 50000:
            reasons.append(
                "High transaction amount"
            )


        if transaction["amount_deviation"] > 30000:
            reasons.append(
                "Unusual amount compared to normal behavior"
            )


        if transaction["is_night_tx"] == 1:
            reasons.append(
                "Night transaction"
            )


        if transaction["tx_within_10min"] == 1:
            reasons.append(
                "Multiple transactions within short time"
            )


        if transaction["location_changed"] == 1:
            reasons.append(
                "Location changed"
            )


        if transaction["device_changed"] == 1:
            reasons.append(
                "New device detected"
            )


        # ================================
        # SAVE TO POSTGRESQL
        # ================================

        conn = get_db_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO fraud_transactions
            (
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
            )

            VALUES
            (
                %s,%s,%s,%s,%s,%s,NOW(),%s,
                %s,%s,%s,%s,%s,%s,%s
            )
            """,

            (
                data.get("transaction_id"),
                data.get("user_id",0),
                transaction["amount"],
                int(probability),

                "Yes" if prediction=="Fraud" else "No",

                ", ".join(reasons),

                1 if prediction=="Fraud" else 0,

                data.get("city","Unknown"),
                data.get("state","Unknown"),
                data.get("merchant_name","Unknown"),
                data.get("merchant_category","Unknown"),
                data.get("payment_method","Unknown"),
                data.get("device","Unknown"),

                risk_level
            )
        )


        conn.commit()

        cursor.close()
        conn.close()


        return JsonResponse({

            "transaction_id":
                data.get("transaction_id"),

            "prediction":
                prediction,

            "fraud_probability":
                probability,

            "confidence":
                confidence,

            "risk_level":
                risk_level,

            "fraud_reasons":
                reasons,

            "database":
                "Transaction saved successfully"

        })


    except Exception as e:

        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )


# ================================
# GET FRAUD TRANSACTIONS
# ================================

def fraud_transactions(request):

    conn = get_db_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
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
        """
    )


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


    return JsonResponse(
        {
            "fraud_transactions": data
        }
    )



# ================================
# DASHBOARD SUMMARY
# ================================

def dashboard_summary(request):

    conn = get_db_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM fraud_transactions"
    )

    total_frauds = cursor.fetchone()[0]



    cursor.execute(
        "SELECT AVG(risk_score) FROM fraud_transactions"
    )

    avg_risk = cursor.fetchone()[0]



    cursor.execute(
        """
        SELECT COUNT(*)
        FROM fraud_transactions
        WHERE risk_score >= 70
        """
    )

    high_risk = cursor.fetchone()[0]



    cursor.execute(
        "SELECT SUM(amount) FROM fraud_transactions"
    )

    total_amount = cursor.fetchone()[0]



    cursor.close()

    conn.close()



    return JsonResponse({

        "total_fraud_transactions":
            total_frauds,

        "average_risk_score":
            round(float(avg_risk), 2)
            if avg_risk else 0,

        "high_risk_transactions":
            high_risk,

        "total_fraud_amount":
            float(total_amount)
            if total_amount else 0

    })



# ================================
# EXPORT CSV
# ================================

def export_fraud_csv(request):

    conn = get_db_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM fraud_transactions
        ORDER BY transaction_time DESC
        LIMIT 100
        """
    )


    rows = cursor.fetchall()


    response = HttpResponse(
        content_type="text/csv"
    )


    response["Content-Disposition"] = (
        'attachment; filename="fraud_transactions.csv"'
    )


    writer = csv.writer(response)


    for row in rows:

        writer.writerow(row)



    cursor.close()

    conn.close()


    return response