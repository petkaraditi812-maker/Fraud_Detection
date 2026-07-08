import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from feature_engineering import load_and_engineer_features
from risk_engine import calculate_risk


def train_fraud_model():
    df = load_and_engineer_features()

    df[["risk_score", "fraud_flag", "risk_level", "fraud_reason"]] = df.apply(
        lambda row: calculate_risk(row),
        axis=1,
        result_type="expand"
    )

    df["fraud_label"] = df["fraud_flag"].map({"No": 0, "Yes": 1})

    features = [
        "amount",
        "amount_deviation",
        "is_night_tx",
        "tx_within_10min",
        "location_changed",
        "device_changed"
    ]

    X = df[features]
    y = df["fraud_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("✅ Model trained successfully")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    os.makedirs("../models", exist_ok=True)

    joblib.dump(model, "../models/fraud_model.pkl")

    print("✅ Model saved at models/fraud_model.pkl")

    return model


if __name__ == "__main__":
    train_fraud_model()