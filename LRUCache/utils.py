import redis

class RedisCache(object):
    def __init__(self, cache_name, host='localhost', port=6379, db=0):
        self.redis = redis.StrictRedis(decode_responses=True, host=host, port=port, db=db)
        self.cache_name = cache_name

    def setRedisConn(self, conn: redis):
        self.redis = conn

    def clear(self):
        return self.redis.flushdb()

    def get(self, key: str):
        return self.redis.hget(self.cache_name, key)

    def getAllKeys(self):
        return self.redis.hgetall(self.cache_name)

    def set(self, key: str, value: str):
        self.redis.hset(self.cache_name, key, value)

    def remove(self, key: any):
        self.redis.hdel(self.cache_name, key)