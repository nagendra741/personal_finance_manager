import sqlite3
from backup.backup_restore import backup_database, restore_database

def test_backup_restore():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Count transactions before backup
    cursor.execute("SELECT COUNT(*) FROM transactions")
    before_backup = cursor.fetchone()[0]

    # Insert test data
    cursor.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (1, 'income', 'Test', 5000, '2025-03-10')")
    conn.commit()
    print("✅ Test data added!")

    # Backup database
    backup_database()
    
    # Count transactions after backup
    cursor.execute("SELECT COUNT(*) FROM transactions")
    after_backup = cursor.fetchone()[0]

    # Delete test data
    cursor.execute("DELETE FROM transactions WHERE category='Test'")
    conn.commit()
    print("❌ Test data deleted from original DB!")

    # Count transactions after deletion
    cursor.execute("SELECT COUNT(*) FROM transactions")
    after_deletion = cursor.fetchone()[0]

    # Restore database
    restore_database()

    # Count transactions after restore
    cursor.execute("SELECT COUNT(*) FROM transactions")
    after_restore = cursor.fetchone()[0]

    conn.close()

    print(f"\n📊 Transactions before restore: {before_backup} | After restore: {after_restore}")

    if before_backup == after_restore:
        print("✅ Restore successful! Data integrity maintained.")
    else:
        print("⚠️ Warning: Transaction count mismatch! Restore may not be complete.")

# Run test
test_backup_restore()
