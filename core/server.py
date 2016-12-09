from flask import Flask
from socketio import Server
from flask_restful import Api

app = Flask("REDIS_VIEWER", static_folder='static', static_url_path='')
sio = Server()
_api = Api(app, prefix='/redis/api')


@app.route("/redis")
def _provide_static():
    return app.send_static_file('index.html')


def register(Resource, route):
    """
    Registers a new application resource
    :param Resource: flask_flask_restful.Resource
    :param route: String
    :return: None
    """
    _api.add_resource(Resource, route)
