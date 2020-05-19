from threading import Timer
from collections import deque

from utils import RedisCache

class LRUCache(object):
    def __init__(self, capacity=128, ttl=0, redis_host='localhost', redis_port=6379, redis_db=0, cache_name='lru', connect=True):
        self.capacity = capacity
        # Cache is a dictionary containing keys and values
        self.cache = {}
        # Queue just contains the keys ordered according to most recently used
        self.queue = deque()
        self.ttl = ttl
        # Connect to the redis cache
        self.redis_conn = RedisCache(cache_name, redis_host, redis_port, redis_db, connect)
        # Get all existing items from redis cache
        if connect:
            self.getItemsFromCache()

    def setRedisConn(self, redis, cache_name):
        self.redis_conn = RedisCache(cache_name=cache_name)
        self.redis_conn.setRedisConn(redis)

    def connectCache(self):
        self.redis_conn.connect()

    def clearCache(self):
        self.redis_conn.clear()
        self._clearNodes()

    def get(self, key: str):
        # Refresh local cache from redis
        self.getItemsFromCache()
        if key not in self.cache:
            return -1
        else:
            return self._getCacheValue(key)

    def peek(self, key: str):
        if key in self.cache:
            return self.cache[key]
        else:
            return -1

    def _getCacheValue(self, key: str):
        value = self.cache[key]
        # Remove the key from redis and queue
        self.queue.remove(key)
        self.redis_conn.remove(key)
        # Append the key again on redis and queue
        self.queue.append(key)
        self.redis_conn.set(key, value)
        # Obtain the value from the node/key
        return value

    def setCapacity(self, n: int):
        self.capacity = n
        while len(self.queue) > self.capacity:
            deletedKey = self.queue.popleft()
            del self.cache[deletedKey]
            self.redis_conn.remove(deletedKey)

    def getItemsFromCache(self):
        self._clearNodes()
        for key, value in self.redis_conn.getAllKeys().items():
            self.cache[key] = value
            self.queue.append(key)

    def put(self, key: str, value: str, ttl=0):
        # Fail first if an invalid argument is given
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("A key or value was not given")
            
        # Refresh local cache from redis
        self.getItemsFromCache()
        
        # Checks queue capacity and removes the last one if full
        self._validateCapacity()
        # Checks if key is in queue; if it is, delete it so it can be refreshed
        self._validateKey(key)
        # Create the key again on the local instance and redis
        self.cache[key] = value
        self.queue.append(key)
        self.redis_conn.set(key, value)
        # Set an expiration time for the key
        self._expireCache(key, ttl)
        return value

    def _validateCapacity(self):
        while len(self.queue) >= self.capacity:
            deletedKey = self.queue.popleft()
            del self.cache[deletedKey]
            self.redis_conn.remove(deletedKey)

    def _validateKey(self, key):
        if key in self.cache:
            self.queue.remove(key)
            self.redis_conn.remove(key)

    def _expireCache(self, key, ttl):
        if ttl > 0:
            # Add an specific expiration time for this record
            Timer(ttl, self._removeCache, [key]).start()
        elif self.ttl > 0:
            # Add the default expiration time for this record if no specific time is given
            Timer(self.ttl, self._removeCache, [key]).start()

    def _clearNodes(self):
        self.queue.clear()
        self.cache.clear()

    def _removeCache(self, *args):
        if args[0] in self.cache:
            self.queue.remove(args[0])
            del self.cache[args[0]]
            self.redis_conn.remove(args[0])