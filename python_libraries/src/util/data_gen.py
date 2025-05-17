import uuid

from faker import Faker

from src.os.env import Env

# Instances of this class are used to generate random data
# such as for unit tests or database loading.
# Chris Joakim, 2025


class DataGenerator:
    def __init__(self):
        self.created_at = int(Env.epoch())
        self.fake = Faker()

    def random_person_document(self, id = None, pk = None):
        doc_id, doc_pk, state = id, pk, self.fake.state()
        if doc_id == None:
            doc_id = str(uuid.uuid4())
        if doc_pk == None:
            doc_pk = state
        return {
            "id": doc_id,
            "pk": doc_pk,
            "name": self.fake.name(),
            "address": self.fake.address(),
            "city": self.fake.city(),
            "state": state,
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "proglang": "python",
            "doctype": "sample"
        }
