"""Utility functions for the ingestion process."""

from fnmatch import fnmatch
from pathlib import Path
from typing import Set


def _should_include(path: Path, base_path: Path, include_patterns: Set[str]) -> bool:
    """
    Determine if the given file or directory path matches any of the include patterns.

    This function checks whether the relative path of a file or directory matches any of the specified patterns. If a
    match is found, it returns `True`, indicating that the file or directory should be included in further processing.

    Parameters
    ----------
    path : Path
        The absolute path of the file or directory to check.
    base_path : Path
        The base directory from which the relative path is calculated.
    include_patterns : Set[str]
        A set of patterns to check against the relative path.

    Returns
    -------
    bool
        `True` if the path matches any of the include patterns, `False` otherwise.
    """
    try:
        rel_path = path.relative_to(base_path)
    except ValueError:
        # If path is not under base_path at all
        return False

    rel_str = str(rel_path)
    if path.is_dir():
        rel_str += "/"

    for pattern in include_patterns:
        if fnmatch(rel_str, pattern):
            return True
    return False


def _should_exclude(path: Path, base_path: Path, ignore_patterns: Set[str]) -> bool:
    """
    Determine if the given file or directory path matches any of the ignore patterns.

    This function checks whether the relative path of a file or directory matches
    any of the specified ignore patterns. If a match is found, it returns `True`, indicating
    that the file or directory should be excluded from further processing.

    Parameters
    ----------
    path : Path
        The absolute path of the file or directory to check.
    base_path : Path
        The base directory from which the relative path is calculated.
    ignore_patterns : Set[str]
        A set of patterns to check against the relative path.

    Returns
    -------
    bool
        `True` if the path matches any of the ignore patterns, `False` otherwise.
    """
    try:
        rel_path = path.relative_to(base_path)
    except ValueError:
        # If path is not under base_path at all
        return True

    rel_str = str(rel_path)
    for pattern in ignore_patterns:
        if pattern and fnmatch(rel_str, pattern):
            return True
    return False
