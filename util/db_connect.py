import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep

# Retry loop every 2 seconds until successful connected to DB
while True:
    try:
        CONN = psycopg2.connect(
            host="172.19.0.1", database="fastapi", user="root", password="root", cursor_factory=RealDictCursor)
        CURSOR = CONN.cursor()
        print("Successfully connected to the database")
        break
    except Exception as error:
        print("Fail to connect to the database")
        print("Error:", error)
        sleep(2)
