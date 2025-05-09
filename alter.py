import sqlite3

# Connect to your existing SQLite DB
conn = sqlite3.connect("donation_platform.db")  # Change name if needed
cursor = conn.cursor()

# Alter the table to add the new column
cursor.execute("ALTER TABLE needs ADD COLUMN image_path TEXT")

# Commit changes and close connection
conn.commit()
conn.close()

print("Column 'image_path' added successfully.")
