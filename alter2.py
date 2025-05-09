import sqlite3

conn = sqlite3.connect("donation_platform.db")
cursor = conn.cursor()

# Add the new address column (if not already present)
try:
    cursor.execute("ALTER TABLE needs ADD COLUMN address TEXT")
    print("✅ Address column added.")
except sqlite3.OperationalError:
    print("✅ Address column already exists.")

conn.commit()
conn.close()
