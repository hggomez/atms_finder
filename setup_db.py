import sqlite3
connection = sqlite3.connect('atms.db')
cursor = connection.cursor()
cursor.execute("alter table 'atms' add column 'remaining_extractions' int default 1000;")