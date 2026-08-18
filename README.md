#  Fraud Detection System

An end-to-end **Machine Learning based Fraud Detection System** that identifies suspicious financial transactions using **Risk Scoring and Logistic Regression**.

##  Project Overview

The system analyses transaction behaviour such as transaction amount, timing, location and device changes to detect potentially fraudulent transactions.

It provides **real-time fraud prediction through a Django API** and stores transaction data using **MongoDB and PostgreSQL**.

##  Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Logistic Regression
* SMOTE
* Django
* MongoDB
* PostgreSQL
* Power BI
* Postman

##  Key Features

* Rule-based fraud risk scoring
* Machine Learning fraud prediction
* SMOTE for handling imbalanced data
* Real-time fraud detection API
* Fraud probability and prediction confidence
* Risk level and fraud reasons
* MongoDB and PostgreSQL integration
* Power BI fraud analysis dashboard

##  Risk Scoring

The system calculates a risk score based on suspicious transaction behaviour.

### Examples:

* High transaction amount
* Large amount deviation
* Night-time transaction
* Multiple transactions within 10 minutes
* Location change
* Device change

Trusted signals such as **OTP verification** and **trusted devices** can reduce the risk score.

##  Machine Learning

The project uses **Logistic Regression** to classify transactions as legitimate or fraudulent.

**SMOTE (Synthetic Minority Oversampling Technique)** is used to handle class imbalance in the training data.

##  API

The Django API provides real-time fraud detection through:

```text
/api/realtime-check/
```

The API returns:

* Fraud prediction
* Fraud probability
* Confidence
* Risk level
* Risk score
* Fraud reasons

##  Database

**MongoDB** → Raw transaction data

**PostgreSQL** → Processed fraud transaction data

##  Dashboard


The processed transaction data is visualized using **Power BI** to analyse fraud patterns and risk levels.
