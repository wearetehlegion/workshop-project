import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
import datetime
import os

# Строка подключения к БД
DB_DSN = os.getenv("DB_DSN")

@contextmanager
def get_connection():
    conn = psycopg2.connect(DB_DSN)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """
    Создаёт схему workshopbot и таблицу users, если они не существуют.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Создать схему, если не существует
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS workshopbot;
            """)
            # Создать таблицу users, если не существует
            cur.execute("""
                CREATE TABLE IF NOT EXISTS workshopbot.users (
                    id SERIAL PRIMARY KEY,
                    username TEXT,
                    user_id TEXT,
                    request TEXT,
                    timestamp TIMESTAMP
                );
            """)
            conn.commit()

def save_user_request(username, user_id, request, timestamp=None):
    """
    Сохраняет данные пользователя и его запрос в таблицу workshopbot.users.
    """
    if timestamp is None:
        timestamp = datetime.datetime.now()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO workshopbot.users (username, user_id, request, timestamp)
                VALUES (%s, %s, %s, %s);
            """, (username, user_id, request, timestamp))
            conn.commit()

def get_user_stats():
    # Здесь должна быть логика получения статистики из БД
    return []