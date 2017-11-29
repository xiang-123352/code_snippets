#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sqlite3

db_filename = 'todo.db'

db_connection= sqlite3.connect(db_filename)

if not os.path.exists(db_filename):
    print("Need to create schema.")
else:
    print("Database exists, assume schema does too.")

db_connection.close
