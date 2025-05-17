import pytest

from src.util.counter import Counter

# pytest -v tests/test_counter.py

def test_all():
    c = Counter()

    assert c.get_data() == {}
    assert c.get_value("Bell") == 0
    c.increment("Bell")
    c.increment("Biv")
    c.increment("DeVoe")

    assert c.get_value("Bell") == 1
    assert c.get_value("Biv") == 1
    assert c.get_value("DeVoe") == 1
    assert c.get_value("Scaggs") == 0

    c.increment("Bell")
    c.increment("Bell")
    c.increment("Bell")
    c.decrement("DeVoe")

    c.decrement("Joakim")
    c.decrement("Joakim")
    c.decrement("Joakim")
    c.increment("Joakim")

    assert c.get_value("Bell") == 4
    assert c.get_value("Biv") == 1
    assert c.get_value("DeVoe") == 0
    assert c.get_value("Joakim") == -2

    c.decrement("DeVoe")
    assert c.get_value("DeVoe") == -1

    assert c.get_data()["Bell"] == 4

    for n in range(10):
        c.increment("Elsa")
    assert c.most_frequent() == 'Elsa'

    for n in range(10):
        c.decrement("Elsa")
    assert c.most_frequent() != 'Elsa'

    c2 = Counter()
    c2.merge(c)
    assert c2.get_data()["Bell"] == 4
    assert c2.get_data()["Elsa"] == 0
    