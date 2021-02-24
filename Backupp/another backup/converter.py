
import csv, sqlite3

con = sqlite3.connect("your_filename.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("CREATE TABLE t (Account, Name);") # use your column names here

with open('test.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin,delimiter=';') # comma is default delimiter
    to_db = [(i['Account'], i['Name']) for i in dr]

cur.executemany("INSERT INTO t (Account, Name) VALUES (?, ?);", to_db)
con.commit()
con.close()