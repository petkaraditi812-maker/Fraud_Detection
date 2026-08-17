Fraud Detection System

An end-to-end Machine Learning based Fraud Detection System that identifies suspicious financial transactions using Risk Scoring and Logistic Regression.

Project Overview

The system analyses transaction behaviour such as amount, transaction timing, location and device changes to detect potentially fraudulent transactions.

It provides real-time fraud prediction through a Django API and stores transaction data using MongoDB and PostgreSQL.

Key Features:
Rule-based fraud risk scoring
Machine Learning fraud prediction
SMOTE for handling imbalanced data
Real-time fraud detection API
Fraud probability and prediction confidence
Risk level and fraud reasons
MongoDB and PostgreSQL integration
Power BI fraud analysis dashboard


Risk Scoring

The system calculates a risk score based on suspicious transaction behaviour.

Examples:

High transaction amount
Large amount deviation
Night-time transaction
Multiple transactions within 10 minutes
Location change
Device change

Trusted signals such as OTP verification and trusted devices can reduce the risk score.
