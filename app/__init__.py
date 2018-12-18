from flask import Flask
from app.config import setup, database

app = Flask(__name__)

setup.initial_setup()

print(database.db_connect("select * from users"))

@app.route('/')
def hello_world():
    return 'Hello World!'


# @app.route('/setup')
# def setup():
#     return 'Hello World! qwe'
