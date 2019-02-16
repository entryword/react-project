import importlib
from datetime import datetime


def import_class(module_class_name):
    module_name, _, class_name = module_class_name.rpartition('.')
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def validate_time_format(time_str, expected_format, err_message=''):
    try:
        datetime.strptime(time_str, expected_format)
    except Exception:
        raise ValueError(err_message)
