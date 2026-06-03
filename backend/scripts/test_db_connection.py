import psycopg2
import os 
from dotenv import load_dotenv

load_dotenv()
Database_password = os.getenv("DATABASE_PASSWORD")
# print(f"Database password: {Database_password}")  # Debugging line to check if the password is loaded correctly
conn = psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    database="movie_recommender",
    user="postgres",
    password=Database_password
)

print("Connection successful!")

conn.close()

