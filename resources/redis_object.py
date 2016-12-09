from flask import jsonify
from flask_restful import request

from core.server import register
from models.RedisKey import RedisKey
from resources.redis_basic_resource import RedisBasicResource


class RedisObjectResource(RedisBasicResource):
    def _get_connection(self):
        return super()._get_connection()

    def get(self):
        key = request.args.get('key')
        super().abort_if_key_doesnt_exist(key)
        value = self._get(key)
        key_type = self._get_type(key)
        key_type = key_type.upper()

        return jsonify(RedisKey(key=key, key_type=key_type, value=value).serialize())

    def post(self):
        body = super()._parser()
        self._set_value(body)

    def put(self):
        body = super()._parser()
        self._set_value(body)
        pass

    def delete(self):
        key = request.args.get('key')
        self._delete(key)

    def _get(self, key):
        redis_client = self._get_connection()
        return redis_client.get(key)

    def _delete(self, key):
        redis_client = self._get_connection()
        redis_client.delete(key)

    def _set_value(self, body):
        redis_client = self._get_connection()
        redis_client.set(body['key'], body['value'])

    def _get_type(self, key):
        redis_client = self._get_connection()
        return redis_client.type(key)


register(RedisObjectResource, '/object')
