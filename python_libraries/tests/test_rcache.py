import pytest

from src.db.rcache import RCache
from src.os.env import Env

# This test assumes that a redis server is running locally,
# such as in WSL.

# pytest -v tests/test_rcache.py

def test_ping_and_client():
    host = Env.redis_host()
    port = Env.redis_port()
    r = RCache(host, port)
    p = r.ping()
    assert p == True
    assert r.client().ping() == True

def test_get_and_set():
    host = Env.redis_host()
    port = Env.redis_port()
    value = "Miles-{}".format(Env.epoch())
    r = RCache(host, port)
    r.set("CAT", value)

    assert value == r.get("CAT").decode('utf-8')
    assert None == r.get("not-there")

    assert value == r.get_str("CAT")
    assert r.get_str("Dog") == None
