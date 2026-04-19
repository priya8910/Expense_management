from flask import Flask, jsonify
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample categories
categories = ["Groceries", "Rent", "Utilities", "Salary", "Transport", "Dining", "Shopping", "Insurance", "Investment", "Others"]

# Generate 50 example transactions
def generate_transactions(n=50):
    transactions = []
    base_date = datetime.now()
    for i in range(n):
        transaction = {
            "id": i + 1,
            "date": (base_date - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d"),
            "description": random.choice(["Uber Ride", "Zomato Order", "Electricity Bill", "Amazon Purchase", "Salary Credit"]),
            "amount": round(random.uniform(-5000, 10000), 2),
            "category": random.choice(categories),
            "account_number": f"ACCT{random.randint(1000, 9999)}"
        }
        transactions.append(transaction)
    return transactions

# In-memory list of transactions
transactions_data = generate_transactions()

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions_data)

if __name__ == '__main__':
    app.run(debug=True)
