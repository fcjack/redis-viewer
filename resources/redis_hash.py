from flask import jsonify
from flask_restful import request

from core.server import register
from models.RedisKey import RedisKey
from resources.redis_basic_resource import RedisBasicResource


class RedisHashResource(RedisBasicResource):
    def get(self):
        operator = request.args.get('operator')
        key = request.args.get('key')
        structure = request.args.get('structure')

        value = self._get(operator, key, structure)
        key_type = "HASH_ELEMENT"

        return jsonify(RedisKey(key=key, key_type=key_type, value=value).serialize())

    def post(self):
        body = super()._parser()
        self._set(body)

    def put(self):
        body = super()._parser()
        self._set(body)

    def delete(self):
        operator = request.args.get('operator')
        key = request.args.get('key')
        structure = request.args.get('structure')
        self._delete(operator, key, structure)
        pass

    def _get(self, operator, key, structure):
        redis_client = super()._get_connection()
        if operator == 'HGET':
            return redis_client.hget(structure, key)

    def _set(self, body):
        redis_client = self._get_connection()
        operator = body['operator']
        if operator == 'HSET':
            redis_client.hset(body['structure'], body['key'], body['value'])

    def _delete(self, operator, key, structure):
        redis_client = self._get_connection()
        if operator == 'HDEL':
            redis_client.hdel(structure, key)
        pass


register(RedisHashResource, '/hash')
