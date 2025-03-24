import sqlite3

def add_income(username, amount, category):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Get user_id from username
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        print(" User not found!")
        return

    user_id = user[0]  # Extract user_id

    # Insert transaction with user_id
    cursor.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, 'income', ?, ?, DATE('now'))",
                   (user_id, category, amount))

    conn.commit()
    conn.close()
    print(" Income added successfully!")

def view_income(username):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Get user_id from username
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if not user:
        print(" User not found!")
        return

    user_id = user[0]  # Extract user_id

    # Fetch transactions using user_id
    cursor.execute("SELECT amount, category, date FROM transactions WHERE user_id = ? AND type = 'income'", (user_id,))
    income_records = cursor.fetchall()

    conn.close()

    if income_records:
        print("\n Income Transactions:")
        for amount, category, date in income_records:
            print(f" {date} | {category}: ₹{amount}")
    else:
        print(" No income records found!")
