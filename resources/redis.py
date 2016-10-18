import json

from flask import jsonify
from flask_restful import Resource, abort, request, reqparse
from redis import StrictRedis

from core.server import register
from models.RedisKey import RedisKey

parser = reqparse.RequestParser()
parser.add_argument('key', type=str, help='Key to set in Redis')
parser.add_argument('value', help='Value to modify on Redis with the key specified')
parser.add_argument('operator', type=str, help='Operator to specify the operation and commando to use')
parser.add_argument('structure', type=str, help='The name of the structure that store the key and value')


# TODO Use this function for each search before the GET, doing a EXISTS command to answer the front
def abort_if_key_doesnt_exist(exists, key):
    if not exists:
        abort(404, message="There is no object with the key {}".format(key))


class RedisResource(Resource):
    strict_redis = None

    # TODO Alter the load the config to a singleton on system and get data from him

    def _get_connection(self):
        if self.strict_redis is not None:
            return self.strict_redis
        else:
            with open("config.json") as json_file:
                config = json.load(json_file)
                _host = config['redis_host']
                _port = config['redis_port']
                self.strict_redis = StrictRedis(host=_host, port=_port, decode_responses='utf-8')

        return self.strict_redis

    def get(self):
        operator = request.args.get('operator')
        key = request.args.get('key')
        structure = request.args.get('structure')
        value = self._get(operator, key, structure)

        if structure is None:
            type = self._get_type(key)
            type = type.upper()
        else:
            type = self._get_type(structure)
            type = type.upper()
            type += "_ELEMENT"

        return jsonify(RedisKey(key=key, key_type=type, value=value).serialize())

    def post(self):
        body = parser.parse_args()
        self._set_value(body)

    def put(self):
        body = parser.parse_args()
        self._set_value(body)
        pass

    def delete(self):
        operator = request.args.get('operator')
        key = request.args.get('key')
        structure = request.args.get('structure')
        self._delete(operator, key, structure)

    def _get(self, operator, key, structure):
        redis_client = self._get_connection()
        if operator == 'GET':
            return redis_client.get(key)
        elif operator == 'HGET':
            return redis_client.hget(structure, key)
        pass

    def _delete(self, operator, key, structure):
        redis_client = self._get_connection()
        if operator == 'DEL':
            redis_client.delete(key)
        elif operator == 'HDEL':
            redis_client.hdel(structure, key)
        pass

    def _set_value(self, body):
        redis_client = self._get_connection()
        operator = body['operator']
        if operator == 'SET':
            redis_client.set(body['key'], body['value'])
        elif operator == 'HSET':
            redis_client.hset(body['structure'], body['key'], body['value'])
        pass

    def _get_type(self, key):
        redis_client = self._get_connection()
        return redis_client.type(key)


register(RedisResource, '/redisop')
