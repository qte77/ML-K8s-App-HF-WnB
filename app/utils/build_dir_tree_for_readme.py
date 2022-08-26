#!/usr/bin/env python
"""
This module outputs a dir tree

Inspired by [Build a Python Directory Tree Generator for the Command Line](\
https://realpython.com/directory-tree-generator-python/\
).

Added

- Do not include entries from `.gitignore`
- `PATH_SEP` instead of `os.sep`

TODO

- Option to show only essential structure with depth = 1
"""

from logging import getLogger
from os.path import abspath, join
from pathlib import Path

from handle_paths import sanitize_path

logger = getLogger(__name__)

PIPE = "│"
ELBOW = "└─"
TEE = "├─"
SPACE_PREFIX = "  "
PIPE_PREFIX = f"{PIPE}{SPACE_PREFIX}"
PATH_SEP = "/"  # {os.sep}

TOGGLE_EXTRA_PIPE = False


class DirectoryTree:
    """TODO"""

    def __init__(self, root_dir):
        """TODO"""
        self._generator = _TreeGenerator(root_dir)

    def generate(self):
        """TODO"""
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


class _TreeGenerator:
    """TODO"""

    def __init__(self, root_dir):
        """TODO"""
        sanitized_path = sanitize_path(abspath(root_dir))
        path = join(sanitized_path["dir"], sanitized_path["base"])
        path_gitignore = join(path, ".gitignore")

        self._tree = []
        self._root_dir = Path(path)
        self._base_dir = sanitized_path["base"]
        with open(path_gitignore) as f:
            self._gitignore = [
                line.strip() for line in f.readlines() if "#" not in line
            ]

    def build_tree(self):
        """TODO"""
        print(self._root_dir)
        logger.debug(self._root_dir)

        self._tree_head()
        self._tree_body(self._root_dir)

        return self._tree

    def _tree_head(self):
        """TODO"""

        self._tree.append(f"{self._base_dir}{PATH_SEP}")
        if TOGGLE_EXTRA_PIPE:
            self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        """TODO"""

        entries = directory.iterdir()
        entries = sorted(entries, key=lambda entry: entry.is_file())
        entries_count = len(entries)

        # TODO loop .gitignore
        for index, entry in enumerate(entries):
            print(f"{entry=}")
            if any(ignore in str(entry) for ignore in self._gitignore):
                print(f"in .gitignore: {entry=}")
            else:
                connector = ELBOW if (index == entries_count - 1) else TEE
                if entry.is_dir():
                    self._add_directory(entry, index, entries_count, prefix, connector)
                else:
                    self._add_file(entry, prefix, connector)

    def _add_directory(self, directory, index, entries_count, prefix, connector):
        """TODO"""

        self._tree.append(f"{prefix}{connector} {directory.name}{PATH_SEP}")

        prefix += PIPE_PREFIX if (index != entries_count) else SPACE_PREFIX

        self._tree_body(
            directory=directory,
            prefix=prefix,
        )

        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        """TODO"""
        self._tree.append(f"{prefix}{connector} {file.name}")
