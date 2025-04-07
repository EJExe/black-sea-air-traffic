import psycopg2
import time 

def DBConnect(retries=10, delay=4):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host="db",
                port=5432,
                dbname="Flights_DB",
                user="postgres",
                password="1234"  
            )
            return conn
        except Exception as e:
            print(f"Connection attempt {i+1} failed: {e}")
            time.sleep(delay)
    return None