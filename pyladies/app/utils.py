import importlib


def import_class(module_class_name):
    module_name, _, class_name = module_class_name.rpartition('.')
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
