from app import sio, app
from flask import render_template


if __name__ == '__main__':
    # app.run()
    sio.run(app, host="10.111.10.9")
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404