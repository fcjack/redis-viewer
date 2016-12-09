import json

from flask.ext.restful import abort
from flask_restful import reqparse, Resource
from redis import StrictRedis


class RedisBasicResource(Resource):
    strict_redis = None
    parser = reqparse.RequestParser()
    parser.add_argument('key', type=str, help='Key to set in Redis')
    parser.add_argument('value', help='Value to modify on Redis with the key specified')
    parser.add_argument('operator', type=str, help='Operator to specify the operation and commando to use')
    parser.add_argument('structure', type=str, help='The name of the structure that store the key and value')

    def __init__(self):
        if self.strict_redis is None:
            self._start_connection()
        pass

    def _start_connection(self):
        with open("config.json") as json_file:
            config = json.load(json_file)
            _host = config['redis_host']
            _port = config['redis_port']
            self.strict_redis = StrictRedis(host=_host, port=_port, decode_responses='utf-8')

    def _get_connection(self):
        if self.strict_redis is not None:
            return self.strict_redis
        else:
            self._start_connection()
        return self.strict_redis

    def _get_type(self, key):
        redis_client = self._get_connection()
        return redis_client.type(key)

    def abort_if_key_doesnt_exist(self, key):
        exists = self._get_connection().exists(key)
        if not exists:
            abort(400, message="There is no object with the key {}".format(key))

    def _parser(self):
        return self.parser.parse_args()
