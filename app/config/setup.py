from app.config import database


def create_users():
    res = database.db_query('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        avatar TEXT,
        background TEXT,
        birth_date TEXT NOT NULL,
        city TEXT NOT NULL,
        country TEXT NOT NULL,
        activation INTEGER DEFAULT 0,
        token TEXT,
        gender TEXT,
        sex_pref TEXT,
        date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP)
        ''')
    if res:
        print(res)
    else:
        print("users created")

def create_about():
    res = database.db_query('''CREATE TABLE IF NOT EXISTS about(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    information TEXT,
    education TEXT,
    work_exp TEXT,
    languages TEXT)''')
    if res:
        print(res)
    else:
        print("about created")

def create_interests():
    res = database.db_query('''CREATE TABLE IF NOT EXISTS interests(
    id_interest INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    title TEXT,
    icon TEXT)''')
    if res:
        print(res)
    else:
        print("interests created")

def create_interests_users():
    res = database.db_query('''CREATE TABLE IF NOT EXISTS interests_users(
    id_interest INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    FOREIGN KEY (id_interest) REFERENCES interests(id_interest) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')
    if res:
        print(res)
    else:
        print("interests created")

# def create_friends():
#     database.db_query('''CREATE TABLE IF NOT EXISTS name (
#     )
#     ''')

# def create_posts():
#     database.db_query('''CREATE TABLE IF NOT EXISTS name (
#     )
#     ''')

def create_likes():
    database.db_query('''CREATE TABLE IF NOT EXISTS name (
    id_user INTEGER NOT NULL,
    id_post INTEGER NOT NULL,
    id_photo INTEGER NOT NULL,
    data_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_post) REFERENCES posts(id_post) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

def create_comments():
    res = database.db_query('''CREATE TABLE IF NOT EXISTS comments(
    id_comment INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    id_post INTEGER NOT NULL,
    text TEXT,
    date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_post) REFERENCES posts(id_post) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')
    if res:
        print(res)
    else:
        print("comments created")

# def create_messages():
#     database.db_query('''CREATE TABLE IF NOT EXISTS name (
#     )
#     ''')



def initial_setup():
    create_users()
    create_about()
    create_interests()
    create_interests_users()
    create_likes()
    create_comments()
