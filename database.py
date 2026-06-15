import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS speeches(
    id SERIAL PRIMARY KEY,
    filename TEXT,
    words INTEGER,
    duration REAL,
    wpm INTEGER,
    filler_count INTEGER,
    score INTEGER
)
""")

conn.commit()

print("Database connected successfully!")

conn.close()