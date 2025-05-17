import pytest

from src.util.bytes import Bytes

# pytest -v tests/test_bytes.py

def test_kilobyte():
    assert Bytes.kilobyte() == 1024

def test_kilobytes():
    assert Bytes.kilobytes(2) == 2048

def test_megabyte():
    assert Bytes.megabyte() == 1048576

def test_megabytes():
    assert Bytes.megabytes(2) == 2097152

def test_megabytes_float():
    assert int(Bytes.megabytes(2.22)) == 2327838

def test_gigabyte():
    assert Bytes.gigabyte() == 1073741824

def test_gigabytes():
    assert Bytes.gigabytes(2) == 2147483648

def test_terabyte():
    assert Bytes.terabyte() == 1099511627776

def test_terabytes():
    assert Bytes.terabytes(2) == 2199023255552

def test_petabyte():
    assert Bytes.petabyte() == 1125899906842624

def test_petabytes():
    assert Bytes.petabytes(2) == 2251799813685248

def test_exabyte():
    assert Bytes.exabyte() == 1152921504606846976

def test_exabytes():
    assert Bytes.exabytes(2) == 2305843009213693952

def test_as_kilobytes():
    n = pow(1024, 1)
    assert Bytes.as_kilobytes(n) == 1.0
    assert Bytes.as_kilobytes(0) == -0.0
    assert Bytes.as_kilobytes(1024) == 1.0
    assert Bytes.as_kilobytes(4096) == 4.0
    assert Bytes.as_kilobytes(10000) == 9.765625

def test_as_megabytes():
    n = pow(1024, 2)
    assert Bytes.as_megabytes(n) == 1.0
    assert Bytes.as_megabytes(0) == 0.0
    assert Bytes.as_megabytes(1048576) == 1.0
    assert Bytes.as_megabytes(13631488) == 13.0
    assert Bytes.as_megabytes(20000000) == 19.073486328125

def test_as_gigabytes():
    n = pow(1024, 3)
    assert Bytes.as_gigabytes(n) == 1.0
    assert Bytes.as_gigabytes(0) == 0.0
    assert Bytes.as_gigabytes(1073741824) == 1.0
    assert Bytes.as_gigabytes(8589934592) == 8.0
    assert Bytes.as_gigabytes(1048576) == 0.0009765625

def test_as_terabytes():
    n = pow(1024, 4)
    assert Bytes.as_terabytes(n) == 1.0

def test_as_petabytes():
    n = pow(1024, 5)
    assert Bytes.as_petabytes(n) == 1.0

def test_as_exabytes():
    n = pow(1024, 6)
    assert Bytes.as_exabytes(n) == 1.0
