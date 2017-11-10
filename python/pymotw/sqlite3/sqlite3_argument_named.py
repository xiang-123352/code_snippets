#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3
import sys

db_filename = 'todo.db'
project = sys.argv[1]

with sqlite3.connect(db_filename) as conn:
    cursor = conn.cursor()
    
    query = """select id, priority, details, status, deadline from task
            where project = :project
            order by deadline, priority
            """
    
    cursor.execute(query, {'project': project})
    
    for row in cursor.fetchall():
        print("%2d [%d] %-25s [%-8s] (%s)" % (row))
