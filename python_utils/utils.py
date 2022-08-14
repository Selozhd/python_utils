import functools
import inspect
from collections import ChainMap


def clean_null_from_list(ls):
    """Cleans elements with value None in a given list."""
    return [i for i in ls if i is not None]


def clean_null_values(dic):
    """Cleans the entries with value None in a given dictionary."""
    return {key: value for key, value in dic.items() if value is not None}


def inverse_dic_lookup(dic, item):
    """Looks up dictionary key using value."""
    return next(key for key, value in dic.items() if value == item)


def join_list_of_dict(ls):
    """Joins a list of dictionaries into a single dictionary."""
    return dict(ChainMap(*ls))


def sort_list_by(iterable, reference):
    """Sorts an iterable with respect to a reference."""
    return [x for _, x in sorted(zip(reference, iterable))]


def ordered(obj):
    """Orders the items of lists and dictionaries."""
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def name_of(obj):
    """Returns the name of function or class."""
    class_name = type(obj).__name__
    if class_name in ['function', 'type']:
        return obj.__name__
    else:
        return class_name


def arguments_of(function):
    """Returns the parameters of the function `function` t."""
    return list(inspect.signature(function).parameters.keys())


def lazy_property(function):
    """Allows adding `@lazy_property` tag to the methods of a class.

    lazy_property avoids recomputing a property over and over.
    The result gets stored in a local var. Computation of the property
    will happen once, on the first call of the property. All
    succeeding calls will use the value stored in the private property.
    """
    attr_name = "_lazy_" + function.__name__

    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, function(self))
        return getattr(self, attr_name)

    return _lazyprop


def unpack_optional_pair(data):
    """Unpacks data tuple.
    Args:
        data: A tuple of the form `(x,)`, or `(x, y)`.
    Returns:
        The unpacked tuple, with `None`s for `y` if it is not provided.
    """
    if isinstance(data, list):
        data = tuple(data)
    if not isinstance(data, tuple):
        return (data, None)
    elif len(data) == 1:
        return (data[0], None)
    elif len(data) == 2:
        return (data[0], data[1])
    else:
        error_msg = ("Data is expected to be in format `x`, `(x,)`, `(x, y)`, "
                     "found: {}").format(data)
        raise ValueError(error_msg)


def unpack_optional_triple(data):
    """Unpacks data tuple.
    Args:
        data: A tuple of the form `(x,)`, `(x, y)`, or `(x, y, z)`.
    Returns:
        The unpacked tuple, with `None`s for `y` and `z` if they are not
        provided.
    """
    if isinstance(data, list):
        data = tuple(data)
    if not isinstance(data, tuple):
        return (data, None, None)
    elif len(data) == 1:
        return (data[0], None, None)
    elif len(data) == 2:
        return (data[0], data[1], None)
    elif len(data) == 3:
        return (data[0], data[1], data[2])
    else:
        error_msg = ("Data is expected to be in format `x`, `(x,)`, `(x, y)`, "
                     "or `(x, y, z)`, found: {}").format(data)
        raise ValueError(error_msg)