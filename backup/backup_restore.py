import os
import shutil
import sqlite3

def count_transactions(db_name):
    """Returns the number of transactions in a database."""
    if not os.path.exists(db_name):
        return 0  # If file doesn't exist, return 0
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def backup_database():
    """Creates a backup of finance.db and verifies its existence."""
    if not os.path.exists("finance.db"):
        print("❌ No database found to back up!")
        return
    
    shutil.copy("finance.db", "backup_finance.db")
    
    if os.path.exists("backup_finance.db"):
        print("✅ Backup completed successfully! File saved as backup_finance.db")
    else:
        print("❌ Backup failed!")

def restore_database():
    """Restores the database from backup and verifies data integrity."""
    if not os.path.exists("backup_finance.db"):
        print("❌ No backup file found! Restore failed.")
        return
    
    original_count = count_transactions("finance.db")
    shutil.copy("backup_finance.db", "finance.db")
    restored_count = count_transactions("finance.db")

    print("✅ Database restored successfully!")
    print(f"📊 Transactions before restore: {original_count} | After restore: {restored_count}")

    if original_count == restored_count:
        print("✅ Data integrity confirmed after restore!")
    else:
        print("⚠️ Warning: Transaction count mismatch! Restore may not be complete.")
