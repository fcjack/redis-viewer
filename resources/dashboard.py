from flask_restful import Resource
from core.server import register


class DashBoard(Resource):
    def get(self):
        return {"hello": "redis viewer", "online": True}


register(DashBoard, '/dashboard')