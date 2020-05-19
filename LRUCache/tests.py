import time
import unittest

import redis
import fakeredis
from cache import LRUCache


class TestVersionComparator(unittest.TestCase):
    def setUp(self):
        server = fakeredis.FakeServer()
        self.redis = fakeredis.FakeStrictRedis(server=server, decode_responses=True)

    def test_error_none_input(self):
        cache = LRUCache(capacity=3, cache_name='lrucache', connect=False)
        cache.setRedisConn(self.redis, cache_name='lrucache')
        with self.assertRaises(ValueError):
            cache.put(None, '1')

    def test_error_not_a_string(self):
        cache = LRUCache(capacity=3, connect=False)
        cache.setRedisConn(self.redis, cache_name='lrucache')
        with self.assertRaises(ValueError):
            cache.put(1, '1')

    def test_lru_cache_cleaning(self):
        cache = LRUCache(capacity=2, connect=False)
        cache.setRedisConn(self.redis, cache_name='lrucache')
        cache.put('1', '1')
        cache.put('2', '2')
        self.assertEqual(cache.get('1'), '1')
        cache.clearCache()
        self.assertEqual(cache.get('2'), -1)
        self.assertEqual(cache.get('1'), -1)

    def test_lru_cache_behavior_without_expiration(self):
        cache = LRUCache(capacity=2, connect=False)
        cache.setRedisConn(self.redis, cache_name='lrucache')
        cache.put('1', '1')
        cache.put('2', '2')
        self.assertEqual(cache.get('1'), '1')
        cache.put('3', '3')
        self.assertEqual(cache.get('2'), -1)
        cache.put('4', '4')
        self.assertEqual(cache.get('3'), '3')
        self.assertEqual(cache.get('4'), '4')
        self.assertEqual(cache.peek('3'), '3')

    def test_lru_cache_behavior_with_default_expiration(self):
        cache = LRUCache(capacity=2, ttl=1, connect=False)
        cache.setRedisConn(self.redis, cache_name='lruexp')
        cache.put('1', '1')
        self.assertEqual(cache.get('1'), '1')
        time.sleep(1.1)
        self.assertEqual(cache.get('1'), -1)

    def test_lru_cache_behavior_with_specific_expiration(self):
        cache = LRUCache(capacity=2, connect=False)
        cache.setRedisConn(self.redis, cache_name='lruwithexp')
        cache.put('2', '2', ttl=1)
        cache.put('1', '1',)
        self.assertEqual(cache.get('1'), '1')
        time.sleep(1.1)
        self.assertEqual(cache.get('2'), -1)
        self.assertEqual(cache.get('1'), '1')

    def test_lru_cache_behavior_with_two_instances(self):
        cache_new_york = LRUCache(capacity=2, connect=False)
        cache_new_york.setRedisConn(self.redis, cache_name='lru')
        cache_bogota = LRUCache(capacity=2, connect=False)
        cache_bogota.setRedisConn(self.redis, cache_name='lru')
        cache_new_york.put('1', '1')
        cache_new_york.put('2', '2')
        self.assertEqual(cache_bogota.get('1'), '1')
        cache_bogota.put('3', '3')
        self.assertEqual(cache_bogota.get('2'), -1)
        cache_bogota.put('4', '4')
        self.assertEqual(cache_new_york.get('3'), '3')
        self.assertEqual(cache_new_york.get('4'), '4')
        self.assertEqual(cache_new_york.peek('3'), '3')

    def test_lru_cache_behavior_default_expiration_with_two_instances(self):
        cache_new_york = LRUCache(capacity=2, ttl=1, connect=False)
        cache_new_york.setRedisConn(self.redis, cache_name='lru')
        cache_bogota = LRUCache(capacity=2, ttl=1, connect=False)
        cache_bogota.setRedisConn(self.redis, cache_name='lru')
        cache_new_york.put('1', '1')
        cache_new_york.put('2', '2')
        self.assertEqual(cache_bogota.get('1'), '1')
        time.sleep(1.1)
        self.assertEqual(cache_bogota.get('2'), -1)

    def test_lru_cache_behavior_specific_expiration_with_two_instances(self):
        cache_montreal = LRUCache(capacity=2, connect=False)
        cache_montreal.setRedisConn(self.redis, cache_name='lru')
        cache_bogota = LRUCache(capacity=2, connect=False)
        cache_bogota.setRedisConn(self.redis, cache_name='lru')
        cache_montreal.put('1', '1')
        cache_montreal.put('2', '2', ttl=1)
        self.assertEqual(cache_bogota.get('1'), '1')
        time.sleep(1.1)
        self.assertEqual(cache_bogota.get('2'), -1)
        self.assertEqual(cache_bogota.get('1'), '1')
        
    def test_lru_cache_behavior_ordering(self):
        cache = LRUCache(capacity=3, connect=False)
        cache.setRedisConn(self.redis, cache_name='lrucache')
        cache.put('1', '1')
        cache.put('2', '2')
        self.assertEqual(cache.get('1'), '1')
        cache.put('3', '3')
        cache.put('4', '4')
        self.assertEqual(cache.get('1'), '1')
        self.assertEqual(cache.get('2'), -1)
        self.assertEqual(cache.get('3'), '3')
        self.assertEqual(cache.get('4'), '4')
        
    def test_lru_cache_json(self):
        cache = LRUCache(capacity=1, connect=False)
        cache.setRedisConn(self.redis, cache_name='lrucache')
        cache.put('1', "{'json':'file'}")
        self.assertEqual(cache.get('1'), "{'json':'file'}")
        
    def test_disconnected_cache(self):
        cache = LRUCache(capacity=1, connect=False)
        with self.assertRaises(NameError):
            cache.get('1')
        with self.assertRaises(redis.exceptions.ConnectionError):
            cache.connectCache()
            cache.get('1')
        
if __name__ == '__main__':
    unittest.main()