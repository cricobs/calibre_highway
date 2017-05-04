import inspect


class PropertyException(Exception):
    def __init__(self, *args, **kwargs):
        name = inspect.stack()[1][3]
        message = "'{0}' property must be implemented".format(name)
        super(PropertyException, self).__init__(message, *args, **kwargs)