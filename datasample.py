import sqlite3

conn = sqlite3.connect('donation_platform.db')
cursor = conn.cursor()

sample_needs = [
    ("Clothes", "Winter jackets needed for children", "City Shelter", "1234567890", 1),
    ("Food", "Dry ration for flood relief", "Village A", "9876543210", 1)
]

cursor.executemany('''
    INSERT INTO needs (need_type, description, place, contact, is_verified)
    VALUES (?, ?, ?, ?, ?)
''', sample_needs)

conn.commit()
conn.close()
print("✅ Sample verified needs added.")
