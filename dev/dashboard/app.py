import callbacks
from layout import app

if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='127.0.0.1',
        port=8080,
    )  # TODO: remove debug, change host and port
