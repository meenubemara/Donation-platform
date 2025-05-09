import sqlite3

try:
    conn = sqlite3.connect('donation_platform.db')
    cursor = conn.cursor()
    print("✅ Connected to database.")

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    print("✅ Users table created.")

    # Create needs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS needs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            need_type TEXT NOT NULL,
            description TEXT,
            place TEXT NOT NULL,
            contact TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0
        )
    ''')
    print("✅ Needs table created.")

    # Create donations table (only once)
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
    print("✅ Donations table created.")

    # Insert default admin
    cursor.execute('''
        INSERT OR IGNORE INTO users (name, email, username, password, is_verified, is_admin)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Admin', 'admin@example.com', 'admin', 'admin123', 1, 1))
    print("✅ Admin user created or already exists.")

    conn.commit()
    print("✅ All changes committed.")
    print("🎉 Database and tables created successfully.")

except Exception as e:
    print("❌ An error occurred:", e)

finally:
    conn.close()
