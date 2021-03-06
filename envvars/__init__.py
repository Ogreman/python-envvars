#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Accepts a file path to an .env file. Parsing the content and adding each
    value into os.environ
"""

import os
import ast

__author__ = 'Matt Seymour'
__email__ = 'matt@mattseymour.net'
__version__ = '0.2.0'


def get(key, default=None):
    """
        Searches os.environ. If a key is found try evaluating its type else;
        return the string.

        returns: k->value (type as defined by ast.literal_eval)
    """
    try:
        return ast.literal_eval(os.environ.get(key.upper(), default))
    except (ValueError, SyntaxError):
        return os.environ.get(key.upper(), default)


def save(filepath=None, **kwargs):
    """
        Saves a list of keyword arguments as environment variables to a file.
        If no filepath given will default to the default `.env` file.
    """
    if filepath is None:
        filepath = os.path.join('.env')

    with open(filepath, 'wb') as file_handle:
        file_handle.writelines(
            '{0}={1}\n'.format(key.upper(), val)
            for key, val in kwargs.items()
        )


def load(filepath=None):
    """
        Reads a .env file into os.environ.

        For a set filepath, open the file and read contents into os.environ.
        If filepath is not set then look in current dir for a .env file.
    """
    if filepath and os.path.exists(filepath):
        pass
    else:
        if not os.path.exists('.env'):
            return
        filepath = os.path.join('.env')

    for key, value in _get_line_(filepath):
        os.environ.setdefault(key, value)


def _get_line_(filepath):
    """
    Gets each line from the file and parse the data.
    Attempt to translate the value into a python type is possible
    (falls back to string).
    """
    for line in open(filepath):
        line = line.strip()
        if line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip().upper()
        value = value.strip()

        if not (key and value):
            continue
        #return line
        yield (key, value)
