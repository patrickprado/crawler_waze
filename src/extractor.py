import json
import MySQLdb

def open_db_connection():
	db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="waze", charset="utf8", use_unicode=True)
        cursor = db.cursor()
      	return cursor,db


def close_db_connection(cursor,db):
	cursor.close()
	db.close()

#creating tables
def creating_table_jams(cursor):
	cursor.execute("CREATE TABLE jams (jam_id INT PRIMARY KEY, block_start_time INT, city VARCHAR(25), block_expiration INT, severity INT, level INT, turn_type VARCHAR(25), type VARCHAR(25), blocking_alert_id INT, delay INT, road_type INT, street VARCHAR(25), update_millis INT, country VARCHAR(25), block_type VARCHAR(25), length INT, block_update INT, speed INT, start_time VARCHAR(50), start_time_millis INT, end_time VARCHAR(50), end_time_millis INT)")

def creating_table_segments_jam(cursor):
	cursor.execute("CREATE TABLE segments_jam (jam_id INT NOT NULL, segment_id INT NOT NULL, from_node INT, is_forward BOOLEAN, to_node INT, PRIMARY KEY(jam_id, segment_id))")

def creating_table_lines_jam(cursor):
	cursor.execute("CREATE TABLE lines_jam (jam_id INT NOT NULL, line_id INT NOT NULL, y FLOAT, x FLOAT, PRIMARY KEY(jam_id, line_id))")

def creating_table_cause_alert_jam(cursor):
	cursor.execute("CREATE TABLE cause_alert_jam (jam_id INT NOT NULL, alert_id VARCHAR(100) NOT NULL, report_rating INT, street VARCHAR(50), magvar INT, speed INT, report_mood INT, city VARCHAR(50), confidence INT, uuid VARCHAR(100), road_type INT, type VARCHAR(50), n_thumbs_up INT, is_jam_unified_alert BOOLEAN, country VARCHAR(10), waze_data VARCHAR(100), subtype VARCHAR(50), inscale BOOLEAN, pub_millis DOUBLE, report_by VARCHAR(50), n_comments INT, show_facebook_pic BOOLEAN, location_x INT, location_y INT, PRIMARY KEY(jam_id, alert_id))")

def creating_table_cause_alert_comments_jam(cursor):
	cursor.execute("CREATE TABLE cause_alert_comments_jam (jam_id INT NOT NULL, alert_id INT NOT NULL, comment_id INT NOT NULL, comment_text VARCHAR(200), report_millis DOUBLE, is_thumbs_up BOOLEAN, report_by VARCHAR(50), PRIMARY KEY(jam_id, alert_id, comment_id))")

def creating_table_alerts(cursor):
	cursor.execute("CREATE TABLE alerts (alert_id VARCHAR(200) PRIMARY KEY, report_rating INT, street VARCHAR(100), magvar INT, speed INT, report_mood INT, city VARCHAR(50), confidence INT, uuid VARCHAR(150), road_type INT, type VARCHAR(100), n_thumbs_up INT, country VARCHAR(20), waze_data VARCHAR(200), subtype VARCHAR(50), inscale BOOLEAN, pub_millis DOUBLE, is_jam_unified_alert BOOLEAN, n_comments INT, show_facebook_pic BOOLEAN, location_x FLOAT, location_y FLOAT)")

def creating_table_comments_alerts(cursor):
	cursor.execute("CREATE TABLE comments_alerts (alert_id VARCHAR(200), comment_id INT NOT NULL, comment_text VARCHAR(200), report_millis DOUBLE, is_thumbs_up BOOLEAN, report_by VARCHAR(50), PRIMARY KEY(alert_id, comment_id))")


#inserting in tables
def insert_jam_db(jam, times, db, cursor):
	if jam.has_key('street'):
		try:
			cursor.execute("INSERT INTO jams (jam_id, city, severity, level, type, delay, road_type, street, update_millis, country, length, speed, start_time, start_time_millis, end_time, end_time_millis) VALUES('%d', '%s', '%d', '%d', '%s', '%d', '%d', '%s', '%d', '%s', '%d', '%d', '%s', '%f', '%s', '%f')" % (jam['id'], jam['city'], jam['severity'], jam['level'], jam['type'], jam['delay'], jam['roadType'], jam['street'], jam['updateMillis'], jam['country'], jam['length'], jam['speed'], times[0], times[1], times[2], times[3]))
			db.commit()
		except:
			pass
	if jam['segments']:
		for segment in jam['segments']:
			try:
				cursor.execute("INSERT INTO segments_jam (jam_id, segment_id, from_node, is_forward, to_node) VALUES('%d', '%d', '%d', '%d', '%d')" % (jam['id'], segment['ID'], segment['fromNode'], segment['isForward'], segment['toNode']))
				db.commit()
			except:
				pass
	


def insert_jam_lines_db(jam, times, db, cursor):

	if jam.has_key('line'):
		for line in xrange(len(jam['line'])):
			try:
				cursor.execute("INSERT INTO lines_jam (jam_id, line_id, y, x) VALUES('%d', '%d', '%f', '%f')" % (jam['id'], line, jam['line'][line]['y'], jam['line'][line]['x']))
				db.commit()
			except:
				pass

def insert_jam_cause_alert_db(jam, times, db, cursor):
	if jam.has_key('causeAlert'):
		causeAlert = jam['causeAlert'] 
		try:
			cursor.execute("INSERT INTO cause_alert_jam (jam_id, alert_id, report_rating, street, magvar, speed, report_mood, city, confidence, uuid, road_type, type, n_thumbs_up, is_jam_unified_alert, country, waze_data, subtype, inscale, pub_millis, report_by, n_comments, show_facebook_pic, location_y, location_x) VALUES('%d', '%s', '%d', '%s', '%d', '%d', '%d', '%s', '%d', '%s', '%d', '%s', '%d', '%d', '%s', '%s', '%s', '%d', '%f', '%s', '%d', '%d', '%d', '%d')" % (jam['id'], causeAlert['id'], causeAlert['reportRating'], causeAlert['street'], causeAlert['magvar'], causeAlert['speed'], causeAlert['reportMood'], causeAlert['city'], causeAlert['confidence'], causeAlert['uuid'], causeAlert['roadType'], causeAlert['type'], causeAlert['nThumbsUp'], causeAlert['isJamUnifiedAlert'], causeAlert['country'], causeAlert['wazeData'], causeAlert['subtype'], causeAlert['inscale'], causeAlert['pubMillis'], causeAlert['reportBy'], causeAlert['nComments'], causeAlert['showFacebookPic'], causeAlert['location']['y'], causeAlert['location']['x']))
			db.commit()
		except:
			pass

def insert_jam_cause_alert_comment_db(jam, times, db, cursor):
	if jam.has_key('comments'):
		for comment in xrange(len(jam['comments'])):
			try:
				cursor.execute("INSERT INTO cause_alert_comments_jam (jam_id, alert_id, comment_id, comment_text, report_millis, is_thumbs_up, report_by) VALUES('%d', '%s', '%d', '%s', '%f', '%d', '%s')" % (jam['id'], jam['causeAlert'], comment, jam['causeAlert']['comments'][comment]['text'], jam['causeAlert']['comments'][comment]['reportMillis'], jam['causeAlert']['comments'][comment]['isThumbsUp'], jam['causeAlert']['comments'][comment]['reportBy']))
				db.commit()
			except:
				pass

def insert_alerts_db(alert, times, db, cursor):
	if alert.has_key('street'):
		try:
			cursor.execute("INSERT INTO alerts (alert_id, report_rating, street, magvar, speed, report_mood, city, confidence, uuid, road_type, type, n_thumbs_up, country, waze_data, subtype, inscale, pub_millis, is_jam_unified_alert, n_comments, show_facebook_pic, location_x, location_y, start_time, start_time_millis, end_time, end_time_millis) VALUES('%s', '%d', '%s', '%d', '%d', '%d', '%s', '%d', '%s', '%d', '%s', '%d', '%s', '%s', '%s', '%d', '%f', '%d', '%d', '%d', '%f', '%f', '%s', '%f', '%s', '%f')" % (alert['id'], alert['reportRating'], alert['street'], alert['magvar'], alert['speed'], alert['reportMood'], alert['city'], alert['confidence'], alert['uuid'], alert['roadType'], alert['type'], alert['nThumbsUp'], alert['country'], alert['wazeData'], alert['subtype'], alert['inscale'], alert['pubMillis'], alert['isJamUnifiedAlert'], alert['nComments'], alert['showFacebookPic'], alert['location']['x'], alert['location']['y'], times[0], times[1], times[2], times[3]))
			db.commit()
		except:
			pass

def insert_comments_alerts_db(alert, times, db, cursor):
	if alert.has_key('comments'):
		for comment in xrange(len(alert['comments'])):
			if alert['comments'][comment].has_key('text'):
				try:
					cursor.execute("INSERT INTO comments_alerts(alert_id, comment_id, comment_text, report_millis, is_thumbs_up, report_by) VALUES('%s', '%d', '%s', '%f', '%d', '%s')" % (alert['id'], comment, alert['comments'][comment]['text'], alert['comments'][comment]['reportMillis'], alert['comments'][comment]['isThumbsUp'], alert['comments'][comment]['reportBy']))
					db.commit()
				except:
					pass
			else:
				try:
					cursor.execute("INSERT INTO comments_alerts(alert_id, comment_id, report_millis, is_thumbs_up, report_by) VALUES('%s', '%d', '%f', '%d', '%s')" % (alert['id'], comment, alert['comments'][comment]['reportMillis'], alert['comments'][comment]['isThumbsUp'], alert['comments'][comment]['reportBy']))
					db.commit()
				except:
					pass

def parser(data):

        cursor, db = open_db_connection()

	times = []
        if data.has_key('startTime'):
                startTime = data['startTime']
		times.append(startTime)

        if data.has_key('startTimeMillis'):
                startTimeMillis = data['startTimeMillis']
		times.append(startTimeMillis)
        if data.has_key('endTime'):
                endTime = data['endTime']
		times.append(endTime)

        if data.has_key('endTimeMillis'):
                endTimeMillis = data['endTimeMillis']
		times.append(startTimeMillis)


        if data.has_key('jams'):
                jams = data['jams']
		#inserting jam data
		for jam in jams:
                        if jam.has_key('city') and jam['city'] == 'Belo Horizonte':
                                insert_jam_db(jam, times, db, cursor)
                                insert_jam_lines_db(jam, times, db, cursor)
                                insert_jam_cause_alert_db(jam, times, db, cursor)
                                insert_jam_cause_alert_comment_db(jam, times, db, cursor)

        if data.has_key('alerts'):
                alerts = data['alerts']
		#inserting alert data
		for alert in alerts:
                        if alert.has_key('city') and alert['city'] == 'Belo Horizonte':
                                insert_alerts_db(alert, times, db, cursor)
                                insert_comments_alerts_db(alert, times, db, cursor)


        close_db_connection(cursor, db)

def create_tables():
        cursor, db = open_db_connection()
        creating_table_jams(cursor)
        creating_table_segments_jam(cursor)
        creating_table_lines_jam(cursor)
        creating_table_cause_alert_jam(cursor)
        creating_table_cause_alert_comments_jam(cursor)
        creating_table_alerts(cursor)
        creating_table_comments_alerts(cursor)
        close_db_connection(cursor, db)

create_tables()
