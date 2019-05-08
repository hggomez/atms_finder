import sqlite3
connection = sqlite3.connect('cajeros-automaticos.db')
cursor = connection.cursor()
cursor.execute("alter table 'cajeros-automaticos' add column 'extracciones_restantes' int default 1000;")