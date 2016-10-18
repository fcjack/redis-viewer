from socketio import Middleware
from core.server import app, sio
from eventlet import wsgi, listen
import json

import resources
import sockets

if __name__ == '__main__':
    with open("config.json") as json_file:
        config = json.load(json_file)

    app = Middleware(sio, app)
    wsgi.server(listen(('', config["port"])), app)
