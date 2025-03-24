import sqlite3

def generate_report(username, period="monthly"):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Get user_id from username
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        print("❌ User not found!")
        return

    user_id = user[0]  # Extract user_id

    # Ensure all amounts are REAL
    cursor.execute("UPDATE transactions SET amount = CAST(amount AS REAL) WHERE type IN ('income', 'expense')")
    conn.commit()

    # Query transactions based on the period
    if period == "monthly":
        cursor.execute("""
            SELECT type, SUM(amount) 
            FROM transactions 
            WHERE user_id=? 
            AND date >= date('now', 'start of month') 
            GROUP BY type
        """, (user_id,))
    elif period == "yearly":
        cursor.execute("""
            SELECT type, SUM(amount) 
            FROM transactions 
            WHERE user_id=? 
            AND date >= date('now', 'start of year') 
            GROUP BY type
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT type, SUM(amount) 
            FROM transactions 
            WHERE user_id=? 
            GROUP BY type
        """, (user_id,))

    report = cursor.fetchall()
    conn.close()

    # Initialize income and expenses
    income, expenses = 0.0, 0.0
    for entry in report:
        if entry[0] == 'income':
            income = float(entry[1] or 0)
        elif entry[0] == 'expense':
            expenses = float(entry[1] or 0)

    savings = income - expenses

    # Print Report
    print("\n📊 Financial Report:")
    print(f"💰 Income: ₹{income}")
    print(f"🛒 Expenses: ₹{expenses}")
    print(f"💾 Savings: ₹{savings}")

    return {"Income": income, "Expenses": expenses, "Savings": savings}
