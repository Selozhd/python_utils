"""Utils for an immutable dataclass data structure."""

import copy
from dataclasses import _process_class


def dataclass(_cls=None,
              *,
              init=True,
              repr=True,
              eq=True,
              order=False,
              unsafe_hash=False,
              frozen=False):
    """Augments a dataclass for efficient creation and immutability."""

    def wrap(cls):
        return _process_class(cls, init, repr, eq, order, unsafe_hash, frozen)

    if _cls is None:
        return wrap
    _cls = _add_dict_with_set_get(_cls)
    return wrap(_cls)


def _add_dict_with_set_get(cls):
    """Add a `data` dictionary to the class, if not already present."""
    if cls.__annotations__.get("data"):
        cls.set = set_
        cls.get = get
    return cls


def set_(self, key, value):
    self.data[key] = value


def get(self, prop, default=None):
    return self.data.get(prop, default)


def fetch_attr(cls, attr, value):
    """Takes any object returns a copy with the attribute changed to value."""
    new_token = copy.copy(cls)
    setattr(new_token, attr, value)
    return new_token


def change_datacls_attr(datacls, attr, func):
    """Changes datacls.attr based on function."""
    datacls = [fetch_attr(token, attr, func(token)) for token in datacls]
    return datacls


def featurize_datacls(datacls, featurizer, feature_name):
    """Calls featurizer on each datacls and writes under feature_name."""
    [token.set(feature_name, featurizer(token.text)) for token in datacls]
    return datacls


def datacls_to_x(datacls, x, default=None):
    """Generalizes the pattern of datacls_to_<x>() functions.
    Args:
        datacls: _LsClsT
        x: key in datacls.data
    Returns:
        List of the "x" key in each datacls data dictionary.
    """
    return [token.get(x, default) for token in datacls]
