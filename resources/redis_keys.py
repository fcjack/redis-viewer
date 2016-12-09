from flask import request

from core.server import register
from models.RedisKey import RedisKey
from resources.redis_basic_resource import RedisBasicResource


class RedisKeysResource(RedisBasicResource):
    def get(self):
        pattern = request.args.get('pattern')
        strict_redis = super()._get_connection()
        result = strict_redis.keys(pattern=pattern)
        to_return = []
        for key in result:
            key_type = strict_redis.type(key)
            to_return.append(RedisKey(key, key_type).serialize())
        return to_return


class RedisScanResource(RedisBasicResource):
    def get(self):
        pattern = request.args.get('pattern')
        count = request.args.get('count')
        strict_redis = super()._get_connection()
        to_return = []
        for key in strict_redis.scan_iter(pattern, count):
            key_type = strict_redis.type(key)
            to_return.append(RedisKey(key, key_type).serialize())
        return to_return


register(RedisKeysResource, '/keys')
register(RedisScanResource, '/scan')
