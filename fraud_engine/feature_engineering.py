import pymongo
import pandas as pd


def load_and_engineer_features():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["fraud_db"]
    collection = db["transactions"]

    data = list(collection.find())
    df = pd.DataFrame(data)

    if df.empty:
        raise ValueError("No transactions found in MongoDB")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["hour"] = df["timestamp"].dt.hour
    df["is_night_tx"] = df["hour"].apply(lambda x: 1 if 0 <= x <= 5 else 0)

    df = df.sort_values(by=["customer_id", "timestamp"])

    df["avg_customer_amount"] = df.groupby("customer_id")["amount"].transform("mean")
    df["amount_deviation"] = df["amount"] - df["avg_customer_amount"]

    df["tx_within_10min"] = (
        df.groupby("customer_id")["timestamp"]
        .diff()
        .dt.total_seconds()
        .fillna(99999)
        .apply(lambda x: 1 if x < 600 else 0)
    )

    df["prev_city"] = df.groupby("customer_id")["city"].shift(1)
    df["location_changed"] = (df["city"] != df["prev_city"]).astype(int)
    df["location_changed"] = df["location_changed"].fillna(0)

    df["prev_device"] = df.groupby("customer_id")["device"].shift(1)
    df["device_changed"] = (df["device"] != df["prev_device"]).astype(int)
    df["device_changed"] = df["device_changed"].fillna(0)

    return df