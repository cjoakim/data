import pytest

from src.os.env import Env
from src.os.system import System

# pytest -v tests/test_system.py

# This method runs once at the beginning of this test module.
@pytest.fixture(scope="session", autouse=True)
def setup_before_all_tests():
    Env.set_unit_testing_environment()

def test_platform_is_windows_is_mac():
    p = System.platform()
    print("platform is: {}".format(p))
    
    if System.is_windows():
        assert System.is_mac() == False
        assert "win" in p  

    if System.is_mac():
        assert System.is_windows() == False
        assert "darwin" in p

    #assert System.is_mac()

def test_cpu_count():
    n = System.cpu_count()
    assert str(type(n)) == "<class 'int'>"
    assert n in [ 4, 8, 12, 16, 32]

def test_cwd():
    s = System.cwd()
    assert str(type(s)) == "<class 'str'>"
    assert s.endswith('core')

def test_pwd():
    s = System.cwd()
    assert str(type(s)) == "<class 'str'>"
    assert s.endswith('core')

def test_hostname():
    host = System.hostname()  # 'Chriss-Mac-Studio.local'
    assert str(type(host)) == "<class 'str'>"
    assert len(host) > 10
    assert len(host) < 30

def test_memory_info():
    info = System.memory_info()  # 'Chriss-Mac-Studio.local'
    print(info)
    # macOS: pmem(rss=43712512, vms=420858331136, pfaults=4203, pageins=0)
    # win11: pmem(rss=85569536, vms=69369856, num_page_faults=24641, peak_wset=86261760, wset=85569536, peak_paged_pool=228416, paged_pool=224448, peak_nonpaged_pool=28752, nonpaged_pool=28144, pagefile=69369856, peak_pagefile=70438912, private=69369856)
    assert str(type(info)) in [
        "<class 'psutil._psosx.pmem'>",
        "<class 'psutil._pswindows.pmem'>" ]
    assert info.rss > 100_000
    assert info.rss < 200_000_000

def test_pid():
    n = System.pid()
    assert str(type(n)) == "<class 'int'>"
    assert n > 1024

def test_platform_info():
    info = System.platform_info()
    print(info)
    # macOS-15.3.2-arm64-arm-64bit : arm
    # Windows-11-10.0.26100-SP0 : Intel64 Family 6 Model 191 Stepping 2, GenuineIntel
    assert str(type(info)) == "<class 'str'>"
    assert '64' in info
    if System.is_mac():
        assert 'macos' in info.lower()
    if System.is_windows():
        assert 'win' in info.lower()

def test_process_name():
    n = System.process_name()
    assert str(type(n)) == "<class 'str'>"
    assert n.lower() in ['python', 'python.exe']

def test_sleep():
    e1 = Env.epoch()
    n = System.sleep(0.5)
    e2 = Env.epoch()
    elapsed = e2 - e1
    print('e1 {} e2 {} elapsed {}'.format(e1, e2, elapsed))
    assert elapsed > 0.4
    assert elapsed < 0.6

def test_get_login():
    s = System.get_login()
    assert str(type(s)) == "<class 'str'>"
    assert s in ['chris', 'cjoakim']

def test_virtual_memory():
    meminfo = System.virtual_memory()
    print(meminfo)
    # macOS: svmem(total=68719476736, available=35310026752, percent=48.6, used=31470387200, free=6896025600, active=28502065152, inactive=26473955328, wired=2968322048)
    assert meminfo.percent > 1.0
    assert meminfo.percent < 100.0
