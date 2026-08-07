import random
import uuid
from datetime import datetime, timedelta
import pymongo
from faker import Faker

fake = Faker("en_IN")

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fraud_db"]
collection = db["transactions"]

# Clear old data
collection.delete_many({})

# City-State Mapping
cities_states = {
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Delhi": "Delhi",
    "Bangalore": "Karnataka",
    "Hyderabad": "Telangana",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan",
    "Nagpur": "Maharashtra"
}

# Lists
devices = ["Android", "iPhone", "Web"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Wallet"]
merchant_categories = [
    "Shopping",
    "Food",
    "Travel",
    "Electronics",
    "Healthcare",
    "Fashion",
    "Recharge"
]

transaction_status = ["Success", "Failed"]

# New Features
otp_verified = [1, 0]
trusted_device = [1, 0]
trusted_beneficiary = [1, 0]

# Merchant Mapping
merchants = {
    "Shopping": ["Amazon", "Flipkart", "Myntra"],
    "Food": ["Zomato", "Swiggy", "Dominos"],
    "Travel": ["MakeMyTrip", "IRCTC", "Uber"],
    "Electronics": ["Croma", "Reliance Digital", "Vijay Sales"],
    "Healthcare": ["Apollo Pharmacy", "PharmEasy", "Tata 1mg"],
    "Fashion": ["Ajio", "Nykaa Fashion", "H&M"],
    "Recharge": ["Paytm", "PhonePe", "Google Pay"]
}

def generate_transaction():
    city = random.choice(list(cities_states.keys()))
    state = cities_states[city]

    category = random.choice(merchant_categories)
    merchant = random.choice(merchants[category])

    customer_id = random.randint(10001, 10150)

    # 15% fraud transactions
    is_fraud = random.random() < 0.15

    if is_fraud:

        amount = random.choice([50000, 80000, 120000])

        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 5),
            minutes=random.randint(0, 59)
        )

        device = random.choice(devices)

        otp_verified = random.choices(
            [0, 1],
            weights=[0.70, 0.30]
        )[0]

        trusted_device = random.choices(
            [0, 1],
            weights=[0.80, 0.20]
        )[0]

        trusted_beneficiary = random.choices(
            [0, 1],
            weights=[0.80, 0.20]
        )[0]

    else:

        amount = random.choice([
            199,
            499,
            799,
            1200,
            2500,
            5000,
            12000,
            25000,
            45000
        ])

        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 90),
            hours=random.randint(6, 23),
            minutes=random.randint(0, 59)
        )

        device = random.choice(devices)

        otp_verified = random.choices(
            [1, 0],
            weights=[0.98, 0.02]
        )[0]

        trusted_device = random.choices(
            [1, 0],
            weights=[0.95, 0.05]
        )[0]

        trusted_beneficiary = random.choices(
            [1, 0],
            weights=[0.90, 0.10]
        )[0]

    return {

        "transaction_id": str(uuid.uuid4()),

        "customer_id": customer_id,

        "amount": amount,

        "timestamp": timestamp,

        "city": city,

        "state": state,

        "device": device,

        "otp_verified": otp_verified,

        "trusted_device": trusted_device,

        "trusted_beneficiary": trusted_beneficiary,

        "payment_method": random.choice(payment_methods),

        "merchant_category": category,

        "merchant_name": merchant,

        "ip_address": fake.ipv4(),

        "transaction_status": random.choices(
            transaction_status,
            weights=[0.95, 0.05]
        )[0]
    }

# Generate 2000 Transactions
transactions = [generate_transaction() for _ in range(2000)]

# Insert into MongoDB
collection.insert_many(transactions)

print("✅ 2000 realistic transactions inserted into MongoDB")