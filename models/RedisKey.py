class RedisKey:
    def __init__(self, key, key_type, value=None):
        self.key = key
        self.key_type = key_type
        self.value = value

    def serialize(self):
        json = {
            "key": self.key,
            "type": self.key_type
        }
        if self.value is not None:
            json.value = self.value
        return json
