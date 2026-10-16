#!/usr/bin/env python3
"""Comment-aware source hashing helpers copied unchanged from the prior core reviewer.
No theorem source or compiler is invoked here.
"""

from pathlib import Path
import hashlib
import json
import re


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def code_only(text):
    result = []
    index = 0
    depth = 0
    while index < len(text):
        if depth:
            if text.startswith('/-', index):
                depth += 1
                result.extend('  ')
                index += 2
            elif text.startswith('-/', index):
                depth -= 1
                result.extend('  ')
                index += 2
            else:
                result.append('\n' if text[index] == '\n' else ' ')
                index += 1
        elif text.startswith('/-', index):
            depth = 1
            result.extend('  ')
            index += 2
        elif text.startswith('--', index):
            end = text.find('\n', index)
            if end < 0:
                end = len(text)
            result.extend(' ' * (end - index))
            index = end
        elif text[index] == '"':
            result.append(' ')
            index += 1
            while index < len(text):
                if text[index] == '\\':
                    result.extend('  ')
                    index += 2
                elif text[index] == '"':
                    result.append(' ')
                    index += 1
                    break
                else:
                    result.append('\n' if text[index] == '\n' else ' ')
                    index += 1
        else:
            result.append(text[index])
            index += 1
    assert depth == 0
    return ''.join(result)

