import json
from . import helper
from . import store

LANG = store._get("NV130") or "en"


def from_i18n():
    with open(helper._PATH_I18N_DIR + f"{LANG}.json", "r", encoding="utf-8") as store:
        return json.load(store)


def to_i18n(data):
    with open(helper._PATH_I18N_DIR + f"{LANG}.json", "w", encoding="utf-8") as store:
        json.dump(data, store, indent=2)


def _all():
    return from_i18n()


def _get(key):
    try:
        data = from_i18n()
        return data[key]
    except KeyError:
        return None


def _set(key, value):
    data = from_i18n()
    data[key] = value
    to_i18n(data)


def _rmv(key):
    try:
        data = from_i18n()
        del data[key]
        to_i18n(data)
    except KeyError:
        return None


def _new(data):
    to_i18n(data)
