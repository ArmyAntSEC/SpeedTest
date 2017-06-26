from __future__ import print_function
import subprocess
import json
import sys
import os
from datetime import datetime
from datetime import tzinfo

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

#-------------------
# Error printing
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

#-------------------
# Function to parse json result returned from speedtest-cli
def parseSTOutput ( resultStr ):
	try: 
		jsonObj = json.loads( resultStr )

		downloadMbps = jsonObj['download']/(1024.0*1024)
		uploadMbps = jsonObj['upload']/(1024.0*1024)	
		timestamp = datetime.strptime( jsonObj['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ' )
	except ValueError:
		eprint ( "Error parsing SpeedTest result:")
		eprint ( resultStr )
		downloadMbps = float('nan')
		uploadMbps = float('nan')
		timestamp = datetime.strptime( '1900-01-01', '%Y-%m-%d' )
	
	return ( {'timestamp': timestamp, 'downloadMbps': downloadMbps, 'uploadMbps': uploadMbps } )	

#-------------------
# Function to call speedtest-cli and get json response
def doSpeedtest():
	if ( 0 ):
		try:		
			proc = subprocess.Popen( ['./speedtest-cli', '--json'], stdout=subprocess.PIPE );		
			result = proc.communicate()						
			stString = result[0]
		except:
			eprint ( "Error calling speedtest-cli" )
			stString = ""
	else:
		stString = '{"bytes_sent": 2678784, "download": 11046830.089912508, "timestamp": "2017-06-24T18:35:33.742058Z", "share": null, "bytes_received": 13884164, "ping": 23.668, "upload": 1346336.9976509183, "server": {"latency": 23.668, "name": "Stockholm", "url": "http://speedtest1.dchosting.se/speedtest/upload.php", "country": "Sweden", "lon": "18.0686", "cc": "SE", "host": "speedtest1.dchosting.se:8080", "sponsor": "Datacom", "url2": "http://speedtest2.dchosting.se/speedtest/upload.php", "lat": "59.3294", "id": "8424", "d": 195.76265185298232}}'
	return stString

#-------------------
# Function that calls speedtest-cli and parses result
def doSpeedTestAndParse():
	stString = doSpeedtest()
	result = parseSTOutput( stString )
	return result

logFileName = './speedtestMeasurementLog.txt'

#-----------------
# Function to write a piece of data to the log file
def writeAMeasurementResult( result ):	

	outputString = "{}\t{}\t{}\n".format( result["timestamp"].strftime('%Y-%m-%dT%H:%M:%S.%fZ'), result["downloadMbps"], result["uploadMbps"] )	
	
	if (os.path.isfile( logFileName) == False):
		fout = open( logFileName, 'w')
		fout.write( 'timestamp\tdownloadMbps\tuploadMbps\n' )
		fout.close()
	
	fout = open( logFileName, 'a')	
	fout.seek(0,os.SEEK_END)
	fout.write( outputString )
	fout.close()

def parseLogFile():
	fin = open( logFileName, 'r' )
	fin.readline() #Read the header line
	
	line = fin.readline()
	while ( line != '' ):
		# Tokenize line and store as three arrays		
		lineSplit = line.split("\t")

		#TODO: add error handling here		
		thisTimestamp = datetime.strptime( lineSplit[0], '%Y-%m-%dT%H:%M:%S.%fZ' )
		thisDownloadMbps = float( lineSplit[1] )
		thisUploadMbps = float( lineSplit[2] )		

		line = fin.readline()
	fin.close()

def makePlots():
	data = parseLogFile()

	# Plot the arrays in data


#-----------------
# Main program
result = doSpeedTestAndParse()
writeAMeasurementResult( result )

# Now make plots
makePlots()

