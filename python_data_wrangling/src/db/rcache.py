import redis

# This class is used to access a Redis cache server, sush as
# a local Redis server, or Azure Cache for Redis.
# See https://redis.readthedocs.io/en/latest/commands.html#core-commands
# Chris Joakim, 2025


class RCache:

    def __init__(self, host, port):
        self.redis_client = redis.Redis(host=host, port=port)

    def set(self, key: str, value):
        """Set the given cache key to the given value."""
        return self.redis_client.set(key, value)

    def get(self, key: str):
        """
        Get the cache value for the given cache key.
        You many need to decode the returned value, like: value.decode('utf-8')
        """
        return self.redis_client.get(key)

    def get_str(self, key: str) -> str | None:
        """Get the str cache value for the given cache key, or None."""
        value = self.redis_client.get(key)
        if value is not None:
            return value.decode('utf-8')
        else:
            return None

    def ping(self):
        """Get the str cache value for the given cache key, or None."""
        return self.redis_client.ping()

    def client(self):
        """Return the redis.Redis client object."""
        return self.redis_client
