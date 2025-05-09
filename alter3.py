import sqlite3

# Connect to your existing SQLite DB
conn = sqlite3.connect("donation_platform.db")  # Change name if needed
cursor = conn.cursor()

# Alter the table to add the new column
cursor.execute("ALTER TABLE users ADD COLUMN aadhaar_image TEXT")
cursor.execute("ALTER TABLE users ADD COLUMN selfie_image TEXT")
cursor.execute("ALTER TABLE users ADD COLUMN aadhaar_verified INTEGER DEFAULT 0")
# Commit changes and close connection
conn.commit()
conn.close()

print("Column 'image_path' added successfully.")
