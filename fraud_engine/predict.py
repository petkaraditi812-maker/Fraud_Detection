import os
import joblib
import pandas as pd


# ================================
# LOAD MODEL
# ================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "fraud_model.pkl"
)

def load_model():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)



# ================================
# FRAUD PREDICTION FUNCTION
# ================================

def predict_fraud(df):

    # Load trained ML model
    model = load_model()


    # Features used during training
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


    # Check missing features

    missing = [
        col for col in features
        if col not in df.columns
    ]


    if missing:

        raise ValueError(
            f"Missing feature columns: {missing}"
        )



    # Select model features

    X = df[features]



    # ================================
    # MODEL PREDICTION
    # ================================

    predictions = model.predict(X)



    # Check probability support

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(X)


        fraud_probability = (
            probabilities[:,1] * 100
        ).round(2)


    else:

        fraud_probability = (
            predictions * 100
        )



    # Store ML prediction

    df["ml_prediction"] = predictions


    # Store fraud probability

    df["fraud_probability"] = (
        fraud_probability
    )



    # ================================
    # CONFIDENCE CALCULATION
    # ================================

    def confidence(prob):

        if prob >= 90:

            return "Very High"


        elif prob >= 75:

            return "High"


        elif prob >= 50:

            return "Medium"


        else:

            return "Low"



    df["prediction_confidence"] = (
        df["fraud_probability"]
        .apply(confidence)
    )



    # ================================
    # CONVERT LABELS
    # ================================

    df["ml_prediction"] = (
        df["ml_prediction"]
        .map({
            0: "Legitimate",
            1: "Fraud"
        })
    )


    return df