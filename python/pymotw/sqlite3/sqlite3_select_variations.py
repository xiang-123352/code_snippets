#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3

db_filename = 'todo.db'

with sqlite3.connect(db_filename) as db_connection:
    db_cursor = db_connection.cursor()
    
    db_cursor.execute("""
        select name, description, deadline from project
        where name = 'pymotw'
    """)
    
    name, description, deadline = db_cursor.fetchone()
    
    print("Project details for {} ({})\n due {}".format(
        description, name, deadline))
    
    db_cursor.execute("""
        select id, priority, details, status, deadline from task
        where project = 'pymotw' order by deadline
    """)
    
    print("\nNext 5 tasks:")
    
    for row in db_cursor.fetchmany(5):
        task_id, priority, details, status, deadline = row
        
        print("{:2d} [{:d}] {:<25} [{:<8}] ({})".format(
            task_id, priority, details, status, deadline))
