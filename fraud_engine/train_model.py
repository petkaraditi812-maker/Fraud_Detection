import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from imblearn.over_sampling import SMOTE

from feature_engineering import load_and_engineer_features
from risk_engine import calculate_risk


def train_fraud_model():

    # Load data
    df = load_and_engineer_features()

    # Calculate risk
    df[["risk_score", "fraud_flag", "risk_level", "action", "fraud_reason"]] = df.apply(
        lambda row: calculate_risk(row),
        axis=1,
        result_type="expand"
    )

    # Create ML labels
    df["fraud_label"] = df["fraud_flag"].map({
        "No": 0,
        "Yes": 1
    })

    # Features
    features = [
        "amount",
        "amount_deviation",
        "is_night_tx",
        "tx_within_10min",
        "location_changed",
        "device_changed",
        "otp_verified",
        "trusted_device",
        "trusted_beneficiary"
    ]

    # Check missing values
    if df[features].isnull().sum().sum() > 0:
        raise ValueError("Missing values found in training features.")

    X = df[features]
    y = df["fraud_label"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y
    )

    # Apply SMOTE ONLY on training data
    smote = SMOTE(random_state=42)
    X_train, y_train = smote.fit_resample(X_train, y_train)

    # Train model
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    # Prediction
    y_pred = model.predict(X_test)

    # Evaluation
    print("\n✅ Model trained successfully\n")

    print("Accuracy:")
    print(accuracy_score(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    os.makedirs("../models", exist_ok=True)

    joblib.dump(model, "../models/fraud_model.pkl")

    print("\n✅ Model saved at models/fraud_model.pkl")

    return model


if __name__ == "__main__":
    train_fraud_model()