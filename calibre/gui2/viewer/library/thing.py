class PropertySetter(object):
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        obj.__dict__[self.func.__name__] = self.func(obj, value) or value


property_setter = PropertySetter
