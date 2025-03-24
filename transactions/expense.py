import sqlite3
from datetime import datetime

def add_expense(username, amount, category):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Get user_id from username
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        print("User not found!")
        conn.close()
        return

    user_id = user[0]
    date = datetime.today().strftime('%Y-%m-%d')

    # Ensure amount is stored as a float
    try:
        amount = float(amount)  # Convert amount to float before storing
    except ValueError:
        print(" Invalid amount entered!")
        conn.close()
        return

    # Insert expense in the correct column order
    cursor.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, 'expense', ?, ?, ?)",
                   (user_id, category, amount, date))

    conn.commit()
    conn.close()

    print("Expense added successfully!")



def view_expense(username):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Get user_id from username
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        print(" User not found!")
        return

    user_id = user[0]  # Extract user_id

    # Fetch expense records
    cursor.execute("SELECT category, amount, date FROM transactions WHERE user_id=? AND type='expense'", (user_id,))
    records = cursor.fetchall()
    
    conn.close()

    if records:
        print("\n🛒 Expense Transactions:")
        for category, amount, date in records:
            print(f"📅 {date} | {category}: ₹{amount}")
    else:
        print("⚠️ No expense records found!")
