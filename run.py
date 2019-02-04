from app import socketio, app


if __name__ == '__main__':
    # app.run()
    socketio.run(app, host="0.0.0.0")
