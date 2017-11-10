#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3

db_filename = 'todo.db'

with sqlite3.connect(db_filename) as db_connection:
    db_cursor = db_connection.cursor()
    
    db_cursor.execute("""
        select * from task where project = 'pymotw'
    """)
    
    print("Task table has these columns:")
    
    print ("name, type, display size, internal size, precision, scale, null flag")
    
    for colinfo in db_cursor.description:
        print(colinfo)
