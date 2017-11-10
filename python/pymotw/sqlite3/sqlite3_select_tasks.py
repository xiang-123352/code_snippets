#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3

db_filename = 'todo.db'

with sqlite3.connect(db_filename) as db_connection:
    db_cursor = db_connection.cursor()
    
    db_cursor.execute("""
        select id, priority, details, status, deadline from task
        where project = 'pymotw'
    """)

    for row in db_cursor.fetchall():
        task_id, priority, details, status, deadline = row

        print('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
        task_id, priority, details, status, deadline))
