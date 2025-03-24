import sqlite3

def set_budget(username, category, limit_amount):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Get user_id from username
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        print(" User not found!")
        conn.close()
        return

    user_id = user[0]

    # Insert or update budget using ON CONFLICT
    cursor.execute("""
        INSERT INTO budgets (user_id, category, limit_amount)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, category) 
        DO UPDATE SET limit_amount = excluded.limit_amount
    """, (user_id, category, limit_amount))

    conn.commit()
    conn.close()
    print(f" Budget set for '{category}' at ₹{limit_amount}!")

def check_budget(username):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Get user_id from username
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        print(" User not found!")
        conn.close()
        return

    user_id = user[0]

    # Check expenses against budget
    cursor.execute("""
        SELECT b.category, b.limit_amount, COALESCE(SUM(t.amount), 0) AS spent
        FROM budgets b
        LEFT JOIN transactions t 
        ON b.user_id = t.user_id 
        AND b.category = t.category 
        AND t.type = 'expense'
        WHERE b.user_id = ?
        GROUP BY b.category, b.limit_amount
    """, (user_id,))

    budgets = cursor.fetchall()
    conn.close()

    if not budgets:
        print(" No budget set!")
        return

    print("\n **Budget Summary:**")
    for category, limit, spent in budgets:
        status = " Within budget" if spent <= limit else " Budget exceeded!"
        print(f" {category}: Spent ₹{spent} / ₹{limit} - {status}")
