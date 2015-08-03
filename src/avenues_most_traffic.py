import MySQLdb
from extractor import *
import string
import operator

def avenues_most_traffic():
  cursor, db = open_db_connection()

  number_street = get_number_jams_by_avenue(db, cursor)

  print number_street

  close_db_connection(cursor, db)


def get_number_jams_by_avenue(db, cursor):
  
  cursor.execute('SELECT street, count(street) FROM jams GROUP BY street ORDER BY count(street)')
  data = cursor.fetchall()

  for d in data:
    print "%s, %d" % (d[0], int(d[1]))

 


avenues_most_traffic()