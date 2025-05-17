import os
import platform
import socket
import time

import psutil

# This class is an interface to platform and system information
# such as memory usage.
# Chris Joakim, 2025


class System:

    @classmethod
    def platform(cls) -> str:
        """
        Return the platform.system() string.
        For example: platform.system() -> 'Darwin'
        """
        return platform.system().lower()

    @classmethod
    def is_windows(cls) -> bool:
        """Return True if the platform is Windows, else False."""
        return "darwin" not in cls.platform()

    @classmethod
    def is_mac(cls) -> bool:
        """Return True if the platform is Apple macOS, else False."""
        return "darwin" in cls.platform()

    @classmethod
    def pid(cls) -> int:
        """Return the current process id int."""
        return os.getpid()

    @classmethod
    def process_name(cls) -> str:
        """Return the current process name."""
        return psutil.Process().name()

    @classmethod
    def get_login(cls) -> str:
        """Return the current user name; os.getlogin()."""
        return os.getlogin()

    @classmethod
    def hostname(cls) -> str:
        """Return the current hostname; socket.gethostname()."""
        return socket.gethostname()

    @classmethod
    def cwd(cls) -> str:
        """Return the current working directory; os.getcwd()"""
        return cls.pwd()
    
    @classmethod
    def pwd(cls) -> str:
        """Return the current working directory; os.getcwd()"""
        return os.getcwd()

    @classmethod
    def platform_info(cls) -> str:
        """Return a string with the platform info including processor."""
        return f"{platform.platform()} : {platform.processor()}"

    @classmethod
    def cpu_count(cls) -> int:
        """Return the number of CPUs on the system."""
        return psutil.cpu_count(logical=False)

    @classmethod
    def memory_info(cls):
        """Return the memory info for the current process."""
        return psutil.Process().memory_info()

    @classmethod
    def virtual_memory(cls):
        """Return the virtual memory info for the current process."""
        return psutil.virtual_memory()

    @classmethod
    def sleep(cls, seconds=1.0) -> None:
        """Sleep for the given number of float seconds."""
        time.sleep(seconds)
