"""Initialize the MySQL database"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from urllib.parse import urlparse


def init_database():
    """Initialize the database using DATABASE_URL"""
    try:
        url = urlparse(settings.DATABASE_URL)

        # SQLite: the file is created automatically
        if url.scheme.startswith("sqlite"):
            print(f"SQLite database configured at: {url.path}")
            print("Database initialization successful!")
            return

        # MySQL: create database if not exists
        import pymysql
        connection = pymysql.connect(
            host=url.hostname or "localhost",
            port=url.port or 3306,
            user=url.username or "root",
            password=url.password or ""
        )
        db_name = url.path.lstrip("/")
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            print(f"Database '{db_name}' created or already exists")
        connection.close()
        print("Database initialization successful!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    init_database()
