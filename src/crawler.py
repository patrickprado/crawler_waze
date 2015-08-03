import json
import urllib2
from extractor import *
import time

def crawlerBeloHorizonte():

	while True:
		link = "https://www.waze.com/row-rtserver/web/GeoRSS?os=60&atof=false&format=JSON&ma=200&mj=100&mu=100&sc=216672&jmu=0&types=alerts%2Cusers%2Ctraffic&left=-44.33354187011719&right=-43.58317565917968&bottom=-19.997372157474384&top=-19.80212896372974&_=1410741556445"
		fin = urllib2.urlopen(link)
		data = json.load(fin)
		parser(data)
		time.sleep(600)


crawlerBeloHorizonte()
