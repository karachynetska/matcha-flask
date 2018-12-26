from app.config import database


def create_users():
    database.db_query('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        avatar TEXT,
        birth_date TEXT NOT NULL,
        city TEXT NOT NULL,
        country TEXT NOT NULL,
        activation INTEGER DEFAULT 0,
        token TEXT,
        gender TEXT,
        sex_pref TEXT,
        date_of_creation TEXT)
        ''')

def create_about():
    database.db_query('''CREATE TABLE IF NOT EXISTS about(
    id INTEGER PRIMARY KEY AUTOINCREMENT
    id_user INTEGER NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    # sex_pref TEXT) ''')

def initial_setup():
    create_users()
    create_about()