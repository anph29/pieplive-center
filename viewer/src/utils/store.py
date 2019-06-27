import json
from . import helper


def from_store():
    with open(helper._STORE_SETTING, 'r', encoding='utf-8') as store:
        return json.load(store)


def to_store(data):
    with open(helper._STORE_SETTING, 'w', encoding='utf-8') as store:
        json.dump(data, store, indent=4)


def _all():
    return from_store()


def _get(key):
    try:
        data = from_store()
        return data[key]
    except KeyError:
        return None


def _set(key, value):
    data = from_store()
    print(data)
    data[key] = value
    to_store(data)


def _rmv(key):
    try:
        data = from_store()
        del data[key]
        to_store(data)
    except KeyError:
        return None


def _new(data):
    to_store(data)
