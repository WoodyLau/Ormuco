import redis

class RedisCache(object):
    def __init__(self, cache_name, host='localhost', port=6379, db=0, connect=True):
        if connect:
            self.redis = redis.StrictRedis(decode_responses=True, host=host, port=port, db=db)
        else:
            self.redis = None
            self.host = host
            self.port = port
            self.db = db
        self.cache_name = cache_name

    def setRedisConn(self, conn: redis):
        self.redis = conn
        
    def connect(self):
        self.redis = redis.StrictRedis(decode_responses=True, host=self.host, port=self.port, db=self.db)

    def clear(self):
        if self.redis == None:
            raise NameError('Cache is not connected, please run connectCache() first')
        return self.redis.flushdb()

    def get(self, key: str):
        if self.redis == None:
            raise NameError('Cache is not connected, please run connectCache() first')
        return self.redis.hget(self.cache_name, key)

    def getAllKeys(self):
        if self.redis == None:
            raise NameError('Cache is not connected, please run connectCache() first')
        return self.redis.hgetall(self.cache_name)

    def set(self, key: str, value: str):
        if self.redis == None:
            raise NameError('Cache is not connected, please run connectCache() first')
        self.redis.hset(self.cache_name, key, value)

    def remove(self, key: any):
        if self.redis == None:
            raise NameError('Cache is not connected, please run connectCache() first')
        self.redis.hdel(self.cache_name, key)