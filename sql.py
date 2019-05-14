import sqlite3

with sqlite3.connect("apidatabase.db") as connection:
    c = connection.cursor()
    c.execute("""DROP TABLE visiters""") #bunu fonksiyona çevir
    c.execute("""CREATE TABLE visiters(name TEXT, surname TEXT)""")
    c.close()

    #connection kapat