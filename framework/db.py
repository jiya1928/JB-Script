import json
import os


class Collection:

    def __init__(self, database, name):
        self.database = database
        self.name = name

        self.records = {}
        self.next_id = 1

        self.load()

    def load(self):
        data = self.database.data.get(
            self.name,
            {}
        )

        self.records = {
            int(key): value
            for key, value in data.get(
                "records",
                {}
            ).items()
        }

        self.next_id = data.get(
            "next_id",
            1
        )

    def save(self):
        self.database.data[self.name] = {
            "records": {
                str(key): value
                for key, value in self.records.items()
            },
            "next_id": self.next_id
        }

        self.database.save()

    def insert(self, data):
        if not isinstance(data, dict):
            raise Exception(
                "insert() expects an object"
            )

        record = dict(data)
        record["id"] = self.next_id

        self.records[self.next_id] = record
        self.next_id += 1

        self.save()

        return dict(record)

    def find(self):
        return [
            dict(record)
            for record in self.records.values()
        ]

    def find_one(self, record_id):
        try:
            record_id = int(record_id)
        except (TypeError, ValueError):
            return None

        record = self.records.get(record_id)

        if record is None:
            return None

        return dict(record)

    def where(self, field, value):
        results = []

        for record in self.records.values():
            if record.get(field) == value:
                results.append(dict(record))

        return results

    def count(self):
        return len(self.records)

    def sort(self, field, descending=False):
        records = [
            dict(record)
            for record in self.records.values()
        ]

        records.sort(
            key=lambda record: (
                record.get(field) is None,
                record.get(field)
            ),
            reverse=bool(descending)
        )

        return records

    def limit(self, amount):
        try:
            amount = int(amount)
        except (TypeError, ValueError):
            raise Exception(
                "limit() expects a number"
            )

        if amount < 0:
            amount = 0

        records = [
            dict(record)
            for record in self.records.values()
        ]

        return records[:amount]

    def update(self, record_id, data):
        try:
            record_id = int(record_id)
        except (TypeError, ValueError):
            return None

        if record_id not in self.records:
            return None

        if not isinstance(data, dict):
            raise Exception(
                "update() expects an object"
            )

        self.records[record_id].update(data)
        self.records[record_id]["id"] = record_id

        self.save()

        return dict(self.records[record_id])

    def delete(self, record_id):
        try:
            record_id = int(record_id)
        except (TypeError, ValueError):
            return None

        record = self.records.pop(
            record_id,
            None
        )

        if record is None:
            return None

        self.save()

        return dict(record)


class Database:

    def __init__(self, filename="jb_data.json"):
        self.filename = filename
        self.data = {}
        self.collections = {}

        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            self.data = {}
            return

        try:
            with open(
                self.filename,
                "r",
                encoding="utf-8"
            ) as file:
                self.data = json.load(file)

        except (json.JSONDecodeError, OSError):
            self.data = {}

    def save(self):
        with open(
            self.filename,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.data,
                file,
                indent=2
            )

    def collection(self, name):
        if name not in self.collections:
            self.collections[name] = Collection(
                self,
                name
            )

        return self.collections[name]


def db():
    return Database()