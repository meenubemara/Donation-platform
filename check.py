import sqlite3
def debug_check_messages_table():
    conn = sqlite3.connect("donation_platform.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
    result = cursor.fetchone()
    conn.close()
    print("✅ Messages table exists." if result else "❌ Messages table does NOT exist.")

debug_check_messages_table()
