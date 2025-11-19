import sqlite3
import pandas as pd

# Load CSV
df = pd.read_csv("hotel_data.csv")

# Connect DB
conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS hotel_data(
    room_number INTEGER PRIMARY KEY,
    room_type TEXT,
    price INTEGER,
    status TEXT
)
""")

# Insert data
df.to_sql("hotel_data", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Data imported successfully!")
