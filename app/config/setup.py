from app.config import database


def initial_setup():

    database.db_connect('''CREATE TABLE IF NOT EXISTS users (
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


[(1, 'ikarkachy', 'qweqwe', 'irina', 'karachynetskaya', 'kuzicka@gail.com', None, '', '', '', 0, None, None, None, None)]
[{'id': 1, 'login': 'ikarkachy', 'password': 'qweqwe', 'firstname': 'irina', 'lastname': 'karachynetskaya',
  'email': 'kuzicka@gail.com', 'avatar': None, 'birth_date': '', 'city': '', 'country': '', 'activation': 0,
  'token': None, 'gender': None, 'sex_pref': None, 'date_of_creation': None}]
