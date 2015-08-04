import MySQLdb
from extractor import *
import string
import operator
import time
import datetime
from constant import *
import pdb
import json

def get_heatmap_data():
  cursor, db = open_db_connection()

  lat_long_jams_per_day = get_start_time_jams(db, cursor)

  print_lat_long_jams_per_day(lat_long_jams_per_day)

  close_db_connection(cursor, db)

def get_start_time_jams(db, cursor):
  
  cursor.execute('SELECT start_time, jam_id FROM jams GROUP BY start_time')
  data = cursor.fetchall()

  h = {}

  for d in data:
    h[d[0]] = str(d[1])
  
  jams_ids = get_jams_id_by_day(h, '15', '03', '2015')

  query  = 'SELECT y, x FROM lines_jam where jam_id IN (%s)'
  params = ', '.join(list(map(lambda x: "%s", jams_ids)))
  query  = query  % params

  cursor.execute(query, jams_ids)
  data = cursor.fetchall()
  
  return data

def get_jams_id_by_day(start_times, day, month, year):

  start_times_by_jam_id = get_start_times_by_jam_id(start_times)

  jams_id = []

  for jam_id in start_times_by_jam_id:
    if start_times_by_jam_id[jam_id]['day'] == day and start_times_by_jam_id[jam_id]['month'] == month and start_times_by_jam_id[jam_id]['year'] == year:
      jams_id.append(jam_id)
  

  return jams_id

def get_start_times_by_jam_id(start_times):
  
  start_times_by_jam_id = {}

  for start_time in start_times:
    date = parse_start_time(start_time)
    jam_id = start_times[start_time]

    start_times_by_jam_id[jam_id] = date  

  return start_times_by_jam_id

def parse_start_time(start_time):

  d = {}
  date, schedule = start_time.split(' ')
  
  d['year'], d['month'], d['day'] = date.split('-')
  d['hour'], d['minute'], d['second'], trash = schedule.split(':')

  return d
  

def print_lat_long_jams_per_day(lat_long_jams_per_day):

  lat_long_heat_map = {}
  lat_long_heat_map["points"] = []

  lat_long_count = count_lat_long(lat_long_jams_per_day)

  for point in lat_long_count:
    h = {}
    h['lat']    = point[0]
    h['lon']    = point[1]
    h['weight'] = lat_long_count[point]

    lat_long_heat_map["points"].append(h)

  f = open('heatmap.json', 'w+')
  f.write(json.dumps(lat_long_heat_map))
  f.close()


def count_lat_long(lat_long_jams_per_day):
  
  lat_long_count = {}

  for point in lat_long_jams_per_day:
    if lat_long_count.has_key(point):
      lat_long_count[point] += 1
    else:
      lat_long_count[point] = 1

  return lat_long_count
  

get_heatmap_data()
  