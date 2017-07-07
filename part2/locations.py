import csv
import sqlite3

conn = sqlite3.connect('locations_v2.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS locations""")
cur.execute("""CREATE TABLE locations
            (parcelid text, latitude text, longitude text)""")

with open('properties_2016_location.csv', 'r') as f:
    reader = csv.reader(f.readlines()[1:])  # exclude header line
    cur.executemany("""INSERT INTO locations VALUES (?,?,?)""",
                    (row for row in reader))
conn.commit()
conn.close()
