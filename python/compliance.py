#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hashlib import md5

SCHEMA_FILE = "importantfile.txt"
HASH_FILE = SCHEMA_FILE + ".md5"

def stored_hash():
    with open(HASH_FILE) as f:
        return f.read()

def calculate_hash():
    hasher = md5()
    with open(SCHEMA_FILE) as f:
        for line in f:
            hasher.update(line)
    return hasher.hexdigest()

if __name__ == '__main__':
    # Update the stored hash if called as script:
    with open(HASH_FILE, "w") as f:
        f.write(calculate_hash())
    print("Hash updated.")
