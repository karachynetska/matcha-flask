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
    background TEXT,
    birth_date TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    activation INTEGER DEFAULT 0,
    token TEXT,
    gender TEXT,
    sex_pref TEXT,
    date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    fame_rating INTEGER DEFAULT 0,
    report INTEGER DEFAULT 0)
    ''')


def create_about():
    database.db_query('''CREATE TABLE IF NOT EXISTS about(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    information TEXT,
    education TEXT,
    work_exp TEXT,
    languages TEXT)''')


def create_education():
    database.db_query('''CREATE TABLE IF NOT EXISTS education(
    id_education INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    university TEXT NOT NULL,
    from_year TEXT NOT NULL,
    to_year TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')


def create_work():
    database.db_query('''CREATE TABLE IF NOT EXISTS job(
    id_job INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    company TEXT NOT NULL,
    designation TEXT NOT NULL,
    from_year TEXT NOT NULL,
    to_year TEXT NOT NULL,
    city TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')


def create_interests():
    database.db_query('''CREATE TABLE IF NOT EXISTS interests(
    id_interest INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    icon TEXT)''')


def create_interests_users():
    database.db_query('''CREATE TABLE IF NOT EXISTS interests_users(
    id_interest INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    FOREIGN KEY (id_interest) REFERENCES interests(id_interest) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')



def create_requests():
    database.db_query('''CREATE TABLE IF NOT EXISTS requests(
    id_request INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sender INTEGER NOT NULL,
    id_taker INTEGER NOT NULL,
    status INTEGER NOT NULL,
    FOREIGN KEY (id_sender) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_taker) REFERENCES users(id) ON DELETE CASCADE)''')


def create_sympathys():
    database.db_query('''CREATE TABLE IF NOT EXISTS sympathys(
    id_user1 INTEGER NOT NULL,
    id_user2 INTEGER NOT NULL,
    FOREIGN KEY (id_user1) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_user2) REFERENCES users(id) ON DELETE CASCADE)''')



def create_photos():
    database.db_query('''CREATE TABLE IF NOT EXISTS photos (
    id_photo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    photo TEXT NOT NULL,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')


def create_likes():
    database.db_query('''CREATE TABLE IF NOT EXISTS likes (
    id_photo INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    data_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_photo) REFERENCES photos(id_photo) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')


def create_dislikes():
    database.db_query('''CREATE TABLE IF NOT EXISTS dislikes (
    id_photo INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    data_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_photo) REFERENCES photos(id_photo) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')


def create_comments():
    database.db_query('''CREATE TABLE IF NOT EXISTS comments(
    id_comment INTEGER PRIMARY KEY AUTOINCREMENT,
    id_photo INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    text TEXT,
    date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_photo) REFERENCES photos(id_photo) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')


def create_dialogues():
    database.db_query('''CREATE TABLE IF NOT EXISTS dialogues(
    id_dialogue INTEGER PRIMARY KEY AUTOINCREMENT,
    dialogue_name TEXT NOT NULL,
    id_user1 INTEGER NOT NULL,
    id_user2 INTEGER NOT NULL,
    FOREIGN KEY (id_user1) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_user2) REFERENCES users(id) ON DELETE CASCADE)''')


def create_messages():
    database.db_query('''CREATE TABLE IF NOT EXISTS messages (
    id_message INTEGER PRIMARY KEY AUTOINCREMENT,
    id_dialogue INTEGER NOT NULL,
    from_whom_id INTEGER NOT NULL,
    to_whom_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT unread,
    date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_dialogue) REFERENCES dialogues(id_dialogue) ON DELETE CASCADE,
    FOREIGN KEY (from_whom_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (to_whom_id) REFERENCES users(id) ON DELETE CASCADE)
    ''')


def create_notifications():
    database.db_query('''CREATE TABLE IF NOT EXISTS notifications (
    id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
    to_whom_id INTEGER NOT NULL,
    notification TEXT,
    notif_type TEXT,
    image TEXT,
    status INT NOT NULL DEFAULT 0,
    date_of_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (to_whom_id) REFERENCES users(id) ON DELETE CASCADE)''')


def create_geolocation():
    database.db_query('''CREATE TABLE IF NOT EXISTS geolocation(
    id_user INTEGER NOT NULL UNIQUE,
    latitude TEXT,
    longitude TEXT,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)''')


def create_blocked_users():
    database.db_query('''CREATE TABLE IF NOT EXISTS blocked_users(
    id_block INTEGER PRIMARY KEY AUTOINCREMENT,
    blocked_user_id INTEGER NOT NULL,
    who_block_id INTEGER NOT NULL,
    FOREIGN KEY (blocked_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (who_block_id) REFERENCES users(id) ON DELETE CASCADE)''')


def initial_setup():
    create_users()
    create_about()
    create_interests()
    create_interests_users()
    create_requests()
    create_sympathys()
    create_photos()
    create_likes()
    create_dislikes()
    create_comments()
    create_dialogues()
    create_messages()
    create_notifications()
    create_education()
    create_work()
    create_geolocation()
    create_blocked_users()