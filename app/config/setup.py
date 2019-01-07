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
    id_user INTEGER NOT NULL)''')
    if res:
        print(res)
    else:
        print("about created")

# def create_friends():
#     database.db_query('''CREATE TABLE IF NOT EXISTS name (
#     )
#     ''')

# def create_posts():
#     database.db_query('''CREATE TABLE IF NOT EXISTS name (
#     )
#     ''')

# def create_likes():
#     database.db_query('''CREATE TABLE IF NOT EXISTS name (
#     )
#     ''')

def create_comments():
    res = database.db_query('''CREATE TABLE IF NOT EXISTS comments(
    id_comment INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    id_post INTEGER NOT NULL,
    text TEXT,
    date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_post) REFERENCES posts(id_post) ON DELETE CASCADE )''')
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
    create_comments()
