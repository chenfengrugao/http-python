#!/usr/bin/env python3

"""
to create test database with sqlite3 format.
"""

import sqlite3

# create db if not exists, and connect
conn = sqlite3.connect("sqlite3.db")

# cursor is a row/record pointer
cursor = conn.cursor()

# create tables
sql = """
create table if not exists test_table
(
id integer primary key autoincrement, 
name varchar(255)
);
"""
cursor.execute(sql)

sql = "insert into test_table (name) values ('Design');"
cursor.execute(sql)
sql = "insert into test_table (name) values ('Verification');"
cursor.execute(sql)
sql = "insert into test_table (name) values ('Backend Implement');"
cursor.execute(sql)

# commit all to database
conn.commit()

# close connection
conn.close()


