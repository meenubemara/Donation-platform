import sqlite3

conn = sqlite3.connect('donation_platform.db')
cursor = conn.cursor()

# Drop old donations table
cursor.execute("DROP TABLE IF EXISTS donations")
print("✅ Old donations table dropped.")

# Create updated donations table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        need_id INTEGER,
        message TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(need_id) REFERENCES needs(id)
    )
''')
print("✅ New donations table created with 'message' column.")

conn.commit()
conn.close()
