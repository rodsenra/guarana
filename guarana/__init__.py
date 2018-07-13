from types import MethodType

from abc import ABC, abstractmethod


class MetaObject(ABC):

    @abstractmethod
    def handle_operation(self, operation, name, attr):
        pass

    @abstractmethod
    def handle_method_call(self, name, func, args, kw):
        pass

    @abstractmethod
    def reconfigure(para_obj, new_meta_obj, old_meta_obj=None):
        pass


def wrap_method(func, name, mo):
    def _wrap(*args, **kw):
        return mo.handle_method_call(name, func, args, kw)
    return _wrap


# This method is injected in the para-object during the reconfigure call
def intercept_attribute_access(self, name):
    try:
        meta_obj = object.__getattribute__(self, '__meta_obj__')
    except AttributeError as ex:
        meta_obj = None
    attr = object.__getattribute__(self, name)
    result = meta_obj.handle_operation('fieldRead', name, attr) if meta_obj else attr
    return result


def reconfigure(para_obj, new_meta_obj, old_meta_obj=None):
    # TODO: notify pre-exisitng meta-cfg of the replacement

    # TODO: negotiate mo replacement
    setattr(para_obj, '__meta_obj__', new_meta_obj)
    for name in [a for a in dir(para_obj) if not a.startswith("__")]:
        attr = object.__getattribute__(para_obj, name)
        if type(attr) == MethodType:
            setattr(para_obj, name, wrap_method(attr, name, new_meta_obj))
    if type(para_obj.__class__) == type:
        setattr(para_obj.__class__, '__getattribute__', intercept_attribute_access)
    return True
