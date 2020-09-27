#!/usr/bin/env python3

import sqlite3

def handle(GET = {}, POST = {}):
    # connect
    conn = sqlite3.connect("sqlite3.db")

    # cursor is a row/record pointer
    cursor = conn.cursor()

    # create tables
    sql = """
    select * from test_table;
    """
    result = cursor.execute(sql)

    data = []
    for row in result:
        temp = {}
        temp['id'] = row[0]
        temp['name'] = row[1]
        data.append(temp)

    return data

