import sqlite3

def check_transactions():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    print("\n All Transactions:")
    
    # Fetch all transactions from the database
    cursor.execute("SELECT id, user_id, type, category, amount, date FROM transactions")
    records = cursor.fetchall()

    if records:
        for record in records:
            print(record)  # Print each transaction as a tuple
    else:
        print(" No transactions found!")

    conn.close()

if __name__ == "__main__":
    check_transactions()
