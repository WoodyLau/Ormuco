========
Overview
========

This is an LRU cache, implemented using a local cache and Redis as a backup for resiliency and geodistribution.

Project
=======

We want to optimize every bits of software we write. Your goal is to write a new library that can be integrated to our stack. Dealing with network issues everyday, latency is our biggest problem. Thus, your challenge is to write a new Geo Distributed LRU (Least Recently Used) cache with time expiration. This library will be used extensively by many of our services so it needs to meet the following criteria::

  1 - Simplicity. Integration needs to be dead simple.
      [covered, this is a standard library]
  2 - Resilient to network failures or crashes.
      [covered, using redis]
  3 - Near real time replication of data across Geolocation. Writes need to be in real time.
      [covered, using redis, replication of the data occurs in near real time and writes on redis are considered in real time]
  4 - Data consistency across regions
      [covered, using redis, the data is always consistent through the database]
  5 - Locality of reference, data should almost always be available from the closest region
      [covered, local will always replicate from redis cache]
  6 - Flexible Schema
      [uses a basic key, value system, with both being strings]
  7 - Cache can expire
      [covered, there is a default timeout in seconds, as well as a specified timeout when using put]


An LRU cache is an efficient cache data structure that can be used to figure out what should be removed when the cache is full. The goal is to always have items accessible in O(1) time.

LRU Cache Implementation
========================

To create the LRU logic were necessary to use the following collections, data structures and tools:



A double-ended queue, or deque, supports adding and removing elements from either end.

collections.deque::
    Returns a new deque object initialized left-to-right (using append()) with data from iterable. If iterable is not specified, the new deque is empty.

Deques are a generalization of stacks and queues (the name is pronounced “deck” and is short for “double-ended queue”). Deques support thread-safe, memory efficient appends and pops from either side of the deque with approximately the same O(1) performance in either direction.

The deque is used to maintain a local ordering of the recently used keys. New/reused keys are appended on the right, and old keys are popped from the left.



A dictionary is used to map or associate things you want to store the keys you need to get them. This will be the actual local cache, so the accessing of it is O(1).


Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes with radius queries and streams.

The Redis hash functionality will be used to support O(1) access of the cache. This is to maintain a backup of the cache that can be accessed across multiple locations and in case a local cache goes down.


Life cycle of the methods
=========================
life-cycle of a PUT::

    Validates the capacity of the cache and remove the Last Recently Used key if no more space is found using the popleft() command
    Validates if the key is in the cache instance and remove that key in order to create it again:
    Create the key on the local instance and redis
    If a ttl(Time to live) was given, the item will expire in that amount of time


life-cycle of a GET::

    Remove the key from the queue and redis cache
    Append the node again on the queue
    Create the key on redis hash again
    Return the value from the cache

The redis cache is accessed whenever a put or get is performed.

=====
Usage
=====

To use Distributed LRU Cache in a project::


	from LRUCache.cache import LRUCache

        lru = LRUCache(capacity=2, cache_name='lrucache', redis_host='localhost', redis_port=6379, redis_db=0, ttl=5)

        lru.put('10', '1')
        lru.put('20', '1', ttl=1)
        lru.get('10')



Where::

   capacity: The capacity of the cache instance (128 by default)
   cache_name: The name of the cache instance to create ('lrucache' by default)
   redis_host: The host name of redis server ('localhost' by default)
   redis_port: The port of redis server (6379 by default)
   redis_db: The database to use on redis (0 by default)
   ttl: time to live, the expiration time (0 by default = No expiration)


methods::

   put: To create a cache item into the cache instance; can have an extra argument (ttl) to expire this specific item
   get: The obtain a cache item altering the order of the items
   peek: The obtain a cache item without altering the order of the items
   setRedisConn: To set a specific redis connection after the item creation
   clearCache: To clear the entire cache instance, both local and redis
   setCapacity: Change the capacity of the cache

Tests
=====

To run the tests, run
::

    python tests.py

Acknowledgements
============

Inspiration for this was taken from https://github.com/pcu4dros/pedro_cuadros_test/tree/master/python-distributed-lru-cache