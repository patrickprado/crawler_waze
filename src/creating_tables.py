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