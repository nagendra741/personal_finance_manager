import sqlite3

def create_tables():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')

    # Transactions Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                        category TEXT NOT NULL,
                        amount REAL NOT NULL,
                        date TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')

    # Budgets Table (Check before creating)
    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        category TEXT NOT NULL,
                        limit_amount REAL NOT NULL,
                        UNIQUE(user_id, category),  --  Ensures uniqueness
                        FOREIGN KEY (user_id) REFERENCES users(id))''')

    cursor.execute("UPDATE transactions SET amount = CAST(amount AS REAL) WHERE type IN ('income', 'expense')")
    conn.commit()

    conn.close()
    print("Database and tables created successfully!")

if __name__ == "__main__":
    create_tables()
