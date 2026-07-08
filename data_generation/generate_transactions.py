import random
import uuid
from datetime import datetime, timedelta
import pymongo
from faker import Faker

fake = Faker("en_IN")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fraud_db"]
collection = db["transactions"]

collection.delete_many({})

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

devices = ["Android", "iPhone", "Web"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Wallet"]
merchant_categories = ["Shopping", "Food", "Travel", "Electronics", "Healthcare", "Fashion", "Recharge"]
transaction_status = ["Success", "Failed"]

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

    amount = random.choice([
        199, 499, 799, 1200, 2500, 5000, 12000,
        25000, 45000, 80000, 120000
    ])

    timestamp = datetime.now() - timedelta(
        days=random.randint(0, 90),
        minutes=random.randint(1, 1440)
    )

    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": random.randint(10001, 10150),
        "amount": amount,
        "timestamp": timestamp,
        "city": city,
        "state": state,
        "device": random.choice(devices),
        "payment_method": random.choice(payment_methods),
        "merchant_category": category,
        "merchant_name": merchant,
        "ip_address": fake.ipv4(),
        "transaction_status": random.choices(transaction_status, weights=[0.9, 0.1])[0]
    }

transactions = [generate_transaction() for _ in range(2000)]
collection.insert_many(transactions)

print("✅ 2000 realistic transactions inserted into MongoDB")