# setup_database.py

import pymysql
from pymysql import OperationalError

def init_db():
    print("📌 Starting init_db() with PyMySQL…")

    try:
        # connect to XAMPP’s MySQL (root, no password)
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            autocommit=True
        )
        print("✅ Connected to MySQL via PyMySQL")

        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS myapp")
            print("✅ Database myapp ensured")
            cursor.execute("USE myapp")
            print("➡ Using database myapp")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY,
                    password VARCHAR(100) NOT NULL
                )
            """)
            print("✅ Table users ensured")

    except OperationalError as e:
        print(f"❌ MySQL OperationalError: {e}")

    except Exception as ex:
        print(f"❌ Unexpected Error: {ex}")

    finally:
        try:
            conn.close()
            print("🔒 Connection closed")
        except:
            pass