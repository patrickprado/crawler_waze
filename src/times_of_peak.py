import MySQLdb
from extractor import *
import string
import operator
import time
import datetime
from constant import *
import pdb

def times_of_peak(day_or_hour):
  cursor, db = open_db_connection()

  jams_by_times_of_peak = get_start_time_jams(db, cursor, day_or_hour)

  print sorted(jams_by_times_of_peak.items(), key=operator.itemgetter(1), reverse=True)

  close_db_connection(cursor, db)


def get_start_time_jams(db, cursor, day_or_hour):
  
  cursor.execute('SELECT start_time, count(start_time) FROM jams GROUP BY start_time')
  data = cursor.fetchall()

  h = {}

  for d in data:
    h[d[0]] = int(d[1])

  #h = sorted(h.items(), key=operator.itemgetter(0))
  
  if day_or_hour == 'hour':
    return get_amount_jams_per_hour(h)
  else:
    return get_amount_jams_per_day(h)

def get_amount_jams_per_hour(start_times):

  h = {}

  for i in range(0, 24):
    h[i] = 0

  for start_time in start_times:
    amount = start_times[start_time]

    d = parse_start_time(start_time)

    if int(d['hour']) - 3 >= 0:
      h[int(d['hour']) - 3] += amount
    else:
      h[int(d['hour']) + 21] += amount


  return h


def get_amount_jams_per_day(start_times):

  days = {}

  for weekday in WEEKDAYS:
    days[WEEKDAYS[weekday]] = 0

  for start_time in start_times:
    amount = start_times[start_time]
    day    = get_weekday_from_start_time(start_time)

    days[WEEKDAYS[day]] += amount

  return days


def parse_start_time(start_time):

  d = {}
  date, schedule = start_time.split(' ')
  
  d['year'], d['month'], d['day'] = date.split('-')
  d['hour'], d['minute'], d['second'], trash = schedule.split(':')

  return d


def get_weekday_from_start_time(start_time):
  
  d = parse_start_time(start_time)

  date_string = ("%d %d %d" % (int(d['day']), int(d['month']), int(d['year'])))

  s = datetime.datetime.strptime(date_string, "%d %m %Y").date()

  return s.weekday()

times_of_peak('day')