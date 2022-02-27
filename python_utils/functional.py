import functools
from typing import Dict


def apply(*func_and_args, **kwargs):
    """Applies a function and returns the results."""
    if not func_and_args:
        raise TypeError('func argument is required')
    func, args = func_and_args[0], func_and_args[1:]
    return func(*args, **kwargs)


def _apply(data, func, **kwargs):
    return func(data, **kwargs)


def pipeline(list_func, data):
    """Pipeline data through a list of functions."""
    return functools.reduce(_apply, list_func, data)


def keymap(func: callable, d: Dict, factory=dict):
    """Applies function to dictionary keys."""
    rv = factory()
    rv.update(zip(map(func, dic.keys()), dic.values()))
    return rv


def valmap(func: callable, d: Dict, factory=dict):
    """Applies function dictionary values."""
    rv = factory()
    rv.update(zip(d.keys(), map(func, d.values())))
    return rv


def itemmap(func: callable, dic: Dict, factory=dict):
    """Applies function to dictionary items."""
    rv = factory()
    rv.update(map(func, dic.items()))
    return rv
