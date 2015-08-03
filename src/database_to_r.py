import json
import MySQLdb
import sys
import datetime

def open_db_connection():
	db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="waze", charset="utf8", use_unicode=True)
        cursor = db.cursor()
      	return cursor,db


def close_db_connection(cursor,db):
	cursor.close()
	db.close()

def array_to_string(tuples):
	string_tuples = ", ".join(map(str, tuples))
	return string_tuples

def select_lon_lat_of_jams(cursor, jams_id="(SELECT jam_id FROM jams)"):
	query = "SELECT x, y FROM lines_jam WHERE jam_id IN (" + jams_id + ")"
	cursor.execute(query)
	lon_lat_jams = cursor.fetchall();
	return lon_lat_jams

def select_start_times(cursor):
	cursor.execute("SELECT start_time FROM jams")
	start_times = cursor.fetchall();
	return start_times
	
def select_jams_of_day(cursor, day):
	query = "SELECT jam_id FROM jams WHERE start_time LIKE '" + day + "%';"


	cursor.execute(query)
	jams_id = cursor.fetchall();
	array_jams_id = []
	for jam_id in jams_id:
		array_jams_id.append(int(jam_id[0]))
	return array_jams_id

def select_jams_of_day_hour_street(cursor, day, hour, street):
	query = "SELECT jam_id FROM jams WHERE start_time LIKE '" + day + " " + str(hour) + "%' and street='" + street + "';"

	cursor.execute(query)
	jams_id = cursor.fetchall();
	array_jams_id = []
	for jam_id in jams_id:
		array_jams_id.append(int(jam_id[0]))
	return array_jams_id


def combine_jams_by_days(cursor):
	jam_ids_by_day = {}
	days = select_lon_lat_of_jams(cursor)
	for day in days:
		jam_ids_by_day[day] = select_jams_of_day(day)
	return jam_ids_by_day


def lon_lat_extractor():
	cursor, db 	 = open_db_connection()
	lon_lat_jams = select_lon_lat_of_jams(cursor)
	identifier 	 = 1
	for lon_lat in lon_lat_jams:
		print identifier, lon_lat[0], lon_lat[1]
		identifier += 1
	close_db_connection(cursor, db)


#para filtrar determinado trecho(como a Av. do Contorno) tem que saber os 
#pontos que estao sendo passados para mudar as clausulas do if

#savassi e gutierrez
def filter_between_lats_lons(lons_lats, lat1, lon1, lat2, lon2):
	
	lons_lats_filtered = []
	for lon_lat in lons_lats:
		lon = float(lon_lat[0])
		lat = float(lon_lat[1])

		#entre o trecho
		if (lat >= lat2 and lat <= lat1) and (lon >= lon2 and lon <= lon1):
			lons_lats_filtered.append([lon, lat])

	return lons_lats_filtered

def lon_lat_by_one_day_extractor():
	cursor, db 	   = open_db_connection()
	
	#horario de verao acabou dia 22 de fevereiro de 2015, entao sao 3 horas de diferenca do banco de dados
	year_month	   = sys.argv[1]#"2015-04-07"
	street 		   = "Av. do Contorno"
	hours 		   = range(15, 21)
	days 		   = range(1, 32)
	#hour  		   = int(sys.argv[2])#18
	for day in days:
		day = format(day, '02')
		day = year_month + "-" + str(day)
			
		for hour in hours:
			hour 		   += 3
			try:
				jams_id 	   = select_jams_of_day_hour_street(cursor, day, hour, street)
				lons_lats 	   = select_lon_lat_of_jams(cursor, array_to_string(jams_id))

				#for lon_lat in lons_lats:
				#	print "%s, %s" % (lon_lat[0], lon_lat[1])
				lat1 = -19.938671
				lon1 = -43.926430
				lat2 = -19.939790
				lon2 = -43.933082

				lons_lats = filter_between_lats_lons(lons_lats, lat1, lon1, lat2, lon2)
				
				amount_jams = 0
				for lon_lat in lons_lats:
					amount_jams += 1
					#print "%s, %s" % (lon_lat[0], lon_lat[1])
				weekday = datetime.datetime.strptime(day, '%Y-%m-%d').strftime('%a')

				print "%s entre Afonso Pena e Savassi, %s, %dh-%dh, %d" % (street, weekday, hour-3, hour-2, amount_jams)
			except:
				pass

	close_db_connection(cursor, db)

lon_lat_by_one_day_extractor()







