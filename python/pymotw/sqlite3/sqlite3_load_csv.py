#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import csv
import sqlite3
import sys

db_filename = 'todo.db'
data_filename = sys.argv[1]

SQL = """
insert into task (details, priority, status, deadline, project)
values (:details, :priority, 'active', :deadline, :project)
"""

with open(data_filename, 'rt') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with sqlite3.connect(db_filename) as connection:
        cursor = connection.cursor()
        cursor.executemany(SQL, csv_reader)
