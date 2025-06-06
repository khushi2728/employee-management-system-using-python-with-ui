import pymysql
from pymysql import OperationalError

def get_connection():
    try:
        return pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="myapp"
        )
    except OperationalError as e:
        print(f"❌ Unable to connect to myapp DB: {e}")
        raise