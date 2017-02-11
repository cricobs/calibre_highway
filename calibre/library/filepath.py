import inspect
import os


def filepath_relative(thing, extension=None):
    try:
        filepath = inspect.getfile(thing.__class__)
    except TypeError:
        try:
            filepath = inspect.getfile(thing)
        except TypeError:
            filepath = thing

    if extension:
        filepath = "{0}.{1}".format(os.path.splitext(filepath)[0], extension.lstrip("."))

    return filepath
