import argparse
import sys

import pytest

from src.os.env import Env
from src.os.system import System

# pytest -v tests/test_env.py

# This method runs once at the beginning of this test module.
@pytest.fixture(scope="session", autouse=True)
def setup_before_all_tests():
    Env.set_unit_testing_environment()

def test_boolean_arg():
    print(sys.argv)
    assert Env.boolean_arg("--some-flag") == True
    assert Env.boolean_arg("--some-other-flag") == False

def test_cosmosdb_emulator_mongo_conn_str():
    expected = "mongodb://localhost:C2y6yDjf5%2FR%2Bob0N8A7Cgv30VRDJIWEHLM%2B4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw%2FJw%3D%3D@localhost:10255/admin?ssl=true"
    assert Env.cosmosdb_emulator_mongo_conn_str() == expected

def test_cosmosdb_nosql_acct():
    value = Env.cosmosdb_nosql_acct()
    assert len(value) > 6
    assert len(value) < 60

def test_cosmosdb_emulator_nosql_key():
    key = Env.cosmosdb_emulator_nosql_key()
    assert len(key) > 80
    assert key.endswith("==")

def test_cosmosdb_emulator_nosql_uri():
    assert Env.cosmosdb_emulator_nosql_uri().startswith("http")

def test_cosmosdb_nosql_authtype():
    expected = "key"
    assert Env.cosmosdb_nosql_authtype() == expected

def test_cosmosdb_nosql_default_container():
    assert Env.cosmosdb_nosql_default_container() == "test"

def test_cosmosdb_nosql_default_database():
    assert Env.cosmosdb_nosql_default_database() == "dev"

def test_cosmosdb_nosql_key():
    key = Env.cosmosdb_nosql_key()
    assert len(key) > 80
    assert key.endswith("==")

def test_cosmosdb_nosql_uri():
    assert Env.cosmosdb_nosql_uri().startswith("http")

def test_envvar():
    assert "jdk" in Env.envvar("JAVA_HOME")
    assert "21"  in Env.envvar("JAVA_HOME")
    assert Env.envvar("MISSING", "42") == "42"
    assert Env.envvar("PI", 3.1415926) == 3.1415926

def test_epoch():
    e1 = Env.epoch()
    assert str(type(e1)) == "<class 'float'>"
    assert e1 > 1700000000.0
    assert e1 < 1750000000.0

def test_log_standard_env_vars():
    assert Env.log_standard_env_vars() == True

def test_mongodb_conn_str():
    expected = Env.cosmosdb_emulator_mongo_conn_str()
    assert Env.mongodb_conn_str().startswith('mongodb://localhost:C2')
    assert Env.mongodb_conn_str() == expected

def test_redis_host():
    expected = "127.0.0.1"
    assert Env.redis_host() == expected

def test_redis_port():
    expected = "6379"
    assert Env.redis_port() == expected

def test_standard_env_vars():
    vars = Env.standard_env_vars()
    keys = sorted(vars.keys())
    print(keys)
    assert 'AZURE_COSMOSDB_NOSQL_ACCT' in keys
    assert 'AZURE_COSMOSDB_NOSQL_URI' in keys
    assert 'AZURE_COSMOSDB_NOSQL_KEY' in keys
    assert 'AZURE_COSMOSDB_NOSQL_AUTHTYPE' in keys
    assert 'AZURE_COSMOSDB_NOSQL_DEFAULT_DB' in keys
    assert 'AZURE_COSMOSDB_NOSQL_DEFAULT_CONTAINER' in keys
    assert 'LOG_LEVEL' in keys
    assert 'MONGO_CONN_STR' in keys
    assert len(keys) > 9
    assert len(keys) < 12
    
def test_username():
    assert Env.username() in ["chris", "cjoakim"]

def test_verbose():
    assert Env.verbose() == True
