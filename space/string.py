from interface import Object
from rpython.rlib.objectmodel import compute_hash
import numbers

class String(Object):
    _immutable_fields_ = ['string[*]']
    __slots__ = ['string']
    def __init__(self, string):
        #assert isinstance(string, unicode)
        self.string = string

    # Not fixing the string here, fix later
    def repr(self):
        return u'"' + self.string + u'"'

    def hash(self):
        return compute_hash(self.string)

    def eq(self, other):
        if isinstance(other, String):
            return self.string == other.string
        return False

    def getattr(self, name):
        if name == u'length':
            return numbers.Integer(len(self.string))
        return Object.getattr(self, name)
