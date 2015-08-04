import sys

LOCAL_TO_INT = { 
"Av. do Contorno entre Gutierrez e Savassi": "A",
"Av. do Contorno entre Gutierrez e Bias Fortes": "B",
"Av. do Contorno entre Bias Fortes e Francisco Sales": "C",
"Av. do Contorno entre Francisco Sales e Afonso Pena": "D",
"Av. do Contorno entre Afonso Pena e Savassi": "E"
}

TIME_PERIOD = {
"15h-16h": "Periodo1516",
"16h-17h": "Periodo1617",
"17h-18h": "Periodo1718",
"18h-19h": "Periodo1819",
"19h-20h": "Periodo1920",
"20h-21h": "Periodo2021"
}

#em kms
SIZE_AVENUES = { 
"Av. do Contorno entre Gutierrez e Savassi": 2.9,
"Av. do Contorno entre Gutierrez e Bias Fortes": 2.1,
"Av. do Contorno entre Bias Fortes e Francisco Sales": 3.0,
"Av. do Contorno entre Francisco Sales e Afonso Pena": 2.4,
"Av. do Contorno entre Afonso Pena e Savassi": 0.75
}

def prepare_data_to_weka():
	f = open(sys.argv[1], 'r')
	lines = f.readlines()

	#import pdb
	#pdb.set_trace()
	
	for line in lines:
		line = line.split(',')
		local = line[0]
		weekday = line[1].split()[0]
		time_period = line[2].split()[0]
		number_jams = int(line[3])

		JAM_LIMIT = 40

		if LOCAL_TO_INT[local] == "E":
			JAM_LIMIT = 15

		#true jam
		if number_jams >= JAM_LIMIT:
			number_jams = "t"
		#false jamss
		else:
			number_jams = "f"

		print "%s,%s,%s,%s" % (LOCAL_TO_INT[local], weekday, TIME_PERIOD[time_period], number_jams)


def calculate_jam_limit(lines):
	for line in lines:
		

prepare_data_to_weka()