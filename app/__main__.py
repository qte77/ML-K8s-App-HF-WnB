#!/usr/bin/env python
"""Redirects to entrypoint of the app"""

from sys import exit

from .app import main

if __name__ == "__main__":
    exit(main(debug_on=False))
