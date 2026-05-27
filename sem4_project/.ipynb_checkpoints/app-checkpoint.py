from flask import Flask, request, render_template, redirect, url_for
import joblib
import pandas as pd
import sqlite3




# Initialize database
conn = sqlite3.connect('expenses.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        amount REAL,
        category TEXT
    )
''')
conn.commit()




app = Flask(__name__)

# Load the model and vectorizer
model = joblib.load('expanse_categorizer_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Sample data storage (can be replaced with a database)
expenses = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/categorize', methods=['POST'])
def categorize():
    description = request.form['description']
    amount = float(request.form['amount'])  # Capture amount for dashboard
    vectorized_text = vectorizer.transform([description])
    predicted_category = model.predict(vectorized_text)[0]

    # Store in the expenses list
    cursor.execute('INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)',
                   (description, amount, predicted_category))
    conn.commit()
    print(f"Description: {description}, Amount: {amount}, Category: {predicted_category}")

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    return render_template('dashboard.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)
