#setupdb.py

import pymysql

def init_db1():
    try:
        # Connect to MySQL server (localhost and port 3306 by default)
        conn = pymysql.connect(
            host="localhost",      # or "127.0.0.1"
            port=3306,             # default port for MySQL
            user="root",           # your MySQL username
            password="",           # your MySQL password
            charset="utf8mb4",
            autocommit=True        # commits automatically
        )

        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS employees12")
        cursor.execute("USE employees12")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(20),
                gender VARCHAR(10),
                dob DATE,
                address TEXT,
                post VARCHAR(100),
                salary FLOAT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')

        print("✅ Database and tables initialized successfully.")
        cursor.close()
        conn.close()

    except pymysql.MySQLError as e:
        print("❌ MySQL Error:", e)

    except Exception as e:
        print("❌ General Error:", e)