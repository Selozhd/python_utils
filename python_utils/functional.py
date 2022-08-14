import functools
from typing import Dict, Callable


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


def keymap(func: Callable, dic: Dict, factory=dict):
    """Applies function to dictionary keys."""
    rv = factory()
    rv.update(zip(map(func, dic.keys()), dic.values()))
    return rv


def valmap(func: Callable, dic: Dict, factory=dict):
    """Applies function dictionary values."""
    rv = factory()
    rv.update(zip(dic.keys(), map(func, dic.values())))
    return rv


def itemmap(func: Callable, dic: Dict, factory=dict):
    """Applies function to dictionary items."""
    rv = factory()
    rv.update(map(func, dic.items()))
    return rv
