from app import sio, app


if __name__ == '__main__':
    # app.run()
    sio.run(app, host="0.0.0.0")
