from app import sio, app


if __name__ == '__main__':
    # app.run()
    sio.run(app, host="10.111.10.9")
