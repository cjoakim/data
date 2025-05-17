
import json
import uuid

from faker import Faker

from src.db.doc_filter import DocFilter
from src.util.data_gen import DataGenerator

# pytest -v tests/test_doc_filter.py

def test_inclusion_and_exclusion():
    dg = DataGenerator()

    # case 1: no inclusions or exclusions, should yield the same doc
    df = DocFilter(None, None)
    doc = dg.random_person_document(None, None)
    filtered = df.filter(doc)
    assert json.dumps(doc, sort_keys=True) ==  json.dumps(filtered, sort_keys=True)

    # case 2: explicit inclusions, and exclusions, with overriding exclusion (address)
    inclusions = "id,pk,name,address,a1".split(",")
    exclusions = "address,a2".split(",")
    df = DocFilter(inclusions, exclusions)
    doc = dg.random_person_document(None, None)
    filtered = df.filter(doc)
    assert len(filtered) == 3
    assert doc['id'] == filtered['id']
    assert doc['pk'] == filtered['pk']
    assert doc['name'] == filtered['name']
