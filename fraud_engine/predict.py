import joblib
import pandas as pd


def predict_fraud(df):
    model = joblib.load("../models/fraud_model.pkl")

    features = [
        "amount",
        "amount_deviation",
        "is_night_tx",
        "tx_within_10min",
        "location_changed",
        "device_changed"
    ]

    X = df[features]

    df["ml_prediction"] = model.predict(X)

    return df