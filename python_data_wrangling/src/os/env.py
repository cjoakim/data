import logging
import os
import sys
import time

from src.os.system import System 

# This class is used to read the host environment variables.
# It also has methods for command-line flag argument processing.
# Chris Joakim, 2025


class Env:

    @classmethod
    def envvar(cls, name: str, default=None) -> str | None:
        """Return the value of the given environment variable name, or None."""
        if name in os.environ:
            return os.environ[name]
        return default

    @classmethod
    def boolean_arg(cls, flag: str) -> bool:
        """Return a boolean indicating if the given arg is in the command-line."""
        for arg in sys.argv:
            if arg == flag:
                return True
        return False

    @classmethod
    def username(cls) -> str | None:
        """Return the USERNAME (Windows) or USER (macOS/Linux) value."""
        user = cls.envvar("USERNAME")
        if user is None:
            user = cls.envvar("USER")
        return user

    @classmethod
    def epoch(cls) -> float:
        """Return the current epoch time, as time.time()"""
        return time.time()

    @classmethod
    def verbose(cls) -> bool:
        """Return a boolean indicating if --verbose is in the command-line."""
        return '--verbose' in sys.argv

    @classmethod
    def cosmosdb_nosql_acct(cls) -> str:
        return cls.envvar("AZURE_COSMOSDB_NOSQL_ACCT", None)

    @classmethod
    def cosmosdb_nosql_uri(cls) -> str:
        value = cls.envvar("AZURE_COSMOSDB_NOSQL_URI", None)
        if value is not None:
            if value.lower().strip() == "emulator":
                return cls.cosmosdb_emulator_nosql_uri()
        return value

    @classmethod
    def cosmosdb_emulator_nosql_uri(cls) -> str:
        if System.is_mac():
            # change to http scheme due to this SSL error:
            # azure.core.exceptions.ServiceRequestError: Cannot connect to host localhost:8081 ssl:False [[SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1000)]
            return "http://localhost:8081"
        else:
            return "https://localhost:8081"
    
    @classmethod
    def cosmosdb_nosql_key(cls) -> str:
        value = cls.envvar("AZURE_COSMOSDB_NOSQL_KEY", None)
        if value is not None:
            if value.lower().strip() == "emulator":
                value = cls.cosmosdb_emulator_nosql_key()
        return value

    @classmethod
    def cosmosdb_emulator_nosql_key(cls) -> str:
        return "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
    
    @classmethod
    def cosmosdb_nosql_authtype(cls) -> str:
        return cls.envvar("AZURE_COSMOSDB_NOSQL_AUTHTYPE", 'key')

    @classmethod
    def cosmosdb_nosql_default_database(cls) -> str:
        return cls.envvar("AZURE_COSMOSDB_NOSQL_DEFAULT_DB", 'dev')

    @classmethod
    def cosmosdb_nosql_default_container(cls) -> str:
        return cls.envvar("AZURE_COSMOSDB_NOSQL_DEFAULT_CONTAINER", 'test')

    @classmethod
    def cosmosdb_emulator_mongo_conn_str(cls) -> str:
        return "mongodb://localhost:C2y6yDjf5%2FR%2Bob0N8A7Cgv30VRDJIWEHLM%2B4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw%2FJw%3D%3D@localhost:10255/admin?ssl=true"

    @classmethod
    def mongodb_conn_str(cls) -> str:
        value = cls.envvar("MONGO_CONN_STR", None)
        if value is not None:
            if value.lower().strip() == "emulator":
                value = cls.cosmosdb_emulator_mongo_conn_str()
        return value

    @classmethod
    def redis_host(cls) -> str:
        return cls.envvar("REDIS_HOST", "127.0.0.1")

    @classmethod
    def redis_port(cls) -> str:
        return cls.envvar("REDIS_PORT", "6379")

    @classmethod
    def log_standard_env_vars(cls) -> bool:
        for key in sorted(cls.standard_env_vars().keys()):
            value = cls.envvar(key)
            logging.warning("envvar: {} -> {}".format(key, value))
        return True

    @classmethod
    def standard_env_vars(cls) -> dict:
        d = dict()
        d["AZURE_COSMOSDB_NOSQL_ACCT"] = "AZURE_COSMOS DB NoSQL account name"
        d["AZURE_COSMOSDB_NOSQL_URI"] = "AZURE_COSMOS DB NoSQL account URI"
        d["AZURE_COSMOSDB_NOSQL_KEY"] = "AZURE_COSMOS DB NoSQL account key"
        d["AZURE_COSMOSDB_NOSQL_AUTHTYPE"] = (
            "Authentication mechanism; key or rbac."
        )
        d["AZURE_COSMOSDB_NOSQL_DEFAULT_DB"] = "AZURE_COSMOS DB NoSQL default database"
        d["AZURE_COSMOSDB_NOSQL_DEFAULT_CONTAINER"] = "AZURE_COSMOS DB NoSQL default container"
        d["LOG_LEVEL"] = (
            "A standard python or java logging level name."
        )
        d["MONGO_CONN_STR"] = (
            "MongoDB connection string for MongoDB or Cosmos DB Mongo vCore, or the emulator"
        )
        d["REDIS_HOST"] = (
            "Redis Cache host, defaults to 127.0.0.1"
        )
        d["REDIS_PORT"] = (
            "Redis Cache port, defaults to 6379"
        )
        return d

    @classmethod
    def set_unit_testing_environment(cls):
        """
        This method is for uniting-testing purposed only.
        It sets sys.argv, and certain environment variables
        for consistent test results.
        See test_env.py for example usage.
        """
        os.environ["AZURE_COSMOSDB_NOSQL_AUTHTYPE"] = "key"
        os.environ["AZURE_COSMOSDB_NOSQL_DEFAULT_DB"] = "dev"
        os.environ["AZURE_COSMOSDB_NOSQL_DEFAULT_CONTAINER"] = "test"
        os.environ["MONGO_CONN_STR"] = "emulator"
        os.environ["REDIS_HOST"] = "127.0.0.1"
        os.environ["REDIS_PORT"] = "6379"

        sys.argv.append('--some-flag')
        sys.argv.append('--some-int')
        sys.argv.append('42')
        sys.argv.append('--some-float')
        sys.argv.append('3.1415926')
        sys.argv.append('--some-float')
        sys.argv.append('--verbose')
        return True
