import psycopg2

from feature_engineering import load_and_engineer_features
from risk_engine import calculate_risk
from predict import predict_fraud


def store_results():

    df = load_and_engineer_features()

    df[["risk_score", "fraud_flag", "risk_level", "fraud_reason"]] = df.apply(
        lambda row: calculate_risk(row),
        axis=1,
        result_type="expand"
    )

    df = predict_fraud(df)

    conn = psycopg2.connect(
        host="localhost",
        database="fraud_analytics",
        user="postgres",
        password="Aditi@123"
    )

    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE fraud_transactions")

    for _, row in df.iterrows():

        if row["fraud_flag"] == "Yes":

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
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        row["transaction_id"],
        row["customer_id"],
        float(row["amount"]),
        int(row["risk_score"]),
        row["fraud_flag"],
        row["fraud_reason"],
        row["timestamp"],
        int(row["ml_prediction"]),
        row["city"],
        row["state"],
        row["merchant_name"],
        row["merchant_category"],
        row["payment_method"],
        row["device"],
        row["risk_level"]
    )
)

    conn.commit()

    cursor.close()
    conn.close()

    print("✅ Fraud transactions stored successfully.")
    print(f"✅ Total Fraud Transactions: {len(df[df['fraud_flag']=='Yes'])}")


if __name__ == "__main__":
    store_results()