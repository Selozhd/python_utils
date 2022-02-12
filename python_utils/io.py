import json
import os
import pickle
import re
import shutil
from pathlib import Path


def read_file(filepath, encoding="utf-8"):
    """Read text from a file."""
    try:
        with open(filepath, encoding=encoding) as f:
            return f.read()
    except FileNotFoundError as e:
        raise ValueError(f"File '{filepath}' does not exist.") from e


def read_json_file(filepath):
    """Read json from a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except ValueError as e:
        abspath = os.path.abspath(filepath)
        raise ValueError(f"Failed to read json from '{abspath}") from e


def json_to_string(js_dic, **kwargs):
    """Converts a dictionary to a string."""
    indent = kwargs.pop("indent", 2)
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(js_dic,
                      indent=indent,
                      ensure_ascii=ensure_ascii,
                      **kwargs)


def write_text_file(content, filepath, encoding='utf-8', append=False):
    """Writes text to a file.
    Args:
        content: The content to write.
        filepath: The path to which the content should be written.
        encoding: The encoding which should be used.
        append: Whether to append to the file or to truncate the file.
    """
    mode = "a" if append else "w"
    with open(filepath, mode, encoding=encoding) as file:
        file.write(content)


def write_json_file(js_obj, filepath, **kwargs):
    """Writes object to a json_file."""
    json_string = json_to_string(js_obj, **kwargs)
    write_text_file(json_string, filepath)


def load_pickle(filepath):
    """Loads an object from pickle."""
    try:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError as e:
        raise ValueError(f"File '{filepath}' does not exist.") from e


def save_pickle(filepath, obj):
    """Saves object to a pickle."""
    with open(filepath, "wb") as f:
        pickle.dump(obj, f)


def delete_directory_tree(filepath):
    shutil.rmtree(filepath)


def _ext_regex(ext):
    return re.compile(f".*(\.{ext})")


def _is_match(regex, string):
    return regex.match(string) is not None


def _any_match(regex_list, string):
    matches = [_is_match(regex, string) for regex in regex_list]
    return any(matches)


def listdir_with_exclusions(path, names=None, ext=None):
    """Lists items in the directory excludes name regexes or extensions."""
    dir_ = Path(path)
    if not dir_.is_dir():
        raise ValueError('path must be a directory.')
    names = names if names else []
    ext = ext if ext else []
    name_regex = [re.compile(expr) for expr in names]
    ext_regex = [_ext_regex(e) for e in ext]
    files = [
        fname for fname in dir_.iterdir()
        if not _any_match(name_regex, fname.name)
    ]
    files = [fname for fname in files if not _any_match(ext_regex, fname.name)]
    return files


def listdir_with_only(path, names=None, ext=None):
    """Lists items in the directory conforming name regexes or extensions."""
    dir_ = Path(path)
    if not dir_.is_dir():
        raise ValueError('path must be a directory.')
    names = names if names else []
    ext = ext if ext else []
    name_regex = [re.compile(expr) for expr in names]
    ext_regex = [_ext_regex(e) for e in ext]
    files_name = set(fname for fname in dir_.iterdir()
                  if _any_match(name_regex, fname.name))
    files_regex = set(fname for fname in dir_.iterdir()
                   if _any_match(ext_regex, fname.name))
    files = list(files_name.union(files_regex))
    return files