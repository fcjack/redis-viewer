class RedisKey:
    def __init__(self, key, key_type, value=None):
        self.key = key
        self.key_type = key_type
        self.value = value

    def serialize(self):
        return {
            "key": self.key,
            "type": self.key_type,
            "value": self.value
        }
