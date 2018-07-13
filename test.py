from guarana import *
import pytest


class MetaDoubler(MetaObject):

    def handle_operation(self, operation, name, attr):
        print("{0} -> {1}({2})".format(operation, name, type(attr)))
        if type(attr) == int:
            return attr * 2
        return attr

    def handle_method_call(self, name, func, args, kw):
        result =  func(*args, **kw)
        print("{0} -> {1}({2}) => {3}".format('method call', name, str(args), str(kw), result))
        return result*2

@pytest.fixture
def dummy_factory():
    "Return para-object that suffers reflection"
    class Dummy:
        x = 1

        def m(self, a, b):
            return a + b
    return Dummy()


class TestMetaObject:
    def test_handle_method_call(self):
        d = dummy_factory()
        mo = MetaDoubler()
        reconfigure(d, mo)
        # capturing para-level interaction in the meta-level
        result = d.m(1, 2)
        assert result == 6, "MetaObject did not changed result"

    def test_handle_fieldRead(self):
        d = dummy_factory()
        mo = MetaDoubler()
        reconfigure(d, mo)
        result = d.x
        assert result == 2, "MetaObject did not changed field"

    def reconfigure(para_obj, new_meta_obj, old_meta_obj=None):
        pass
