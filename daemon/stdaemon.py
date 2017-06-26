from __future__ import print_function
import subprocess
import json
import sys
import os
import time
import signal
from datetime import datetime
from datetime import tzinfo

import sys
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

#-----------------
# Function to write a piece of data to the log file
def writeAMeasurementResult( result ):
	fileName = './measurementLog.txt'

	outputString = "{}\t{}\t{}\n".format( result["timestamp"].strftime('%Y-%m-%dT%H:%M:%S.%fZ'), result["downloadMbps"], result["uploadMbps"] )	
	
	if (os.path.isfile( fileName) == False):
		fout = open( fileName, 'w')
		fout.write( 'timestamp\tdownloadMbps\tuploadMbps\n' )
		fout.close()
	
	fout = open( fileName, 'a')	
	fout.seek(0,os.SEEK_END)
	fout.write( outputString )
	fout.close()

#-----------------
#signal handler to catch sigint
def catchSigInt( signal, frame ):
	global shouldTerm
	shouldTerm = True

#-----------------
# Function to do repeated measurements
def doRepeatedMeasurements( ):
	global shouldTerm
	shouldTerm = False

	while shouldTerm == False:
		start_time = time.time()
		result = doSpeedTestAndParse()
		writeAMeasurementResult( result )        	
		print ( result )

		elapsed_time = time.time() - start_time			
		time.sleep ( 60*60 - elapsed_time )

	eprint ( "Main loop ended" )		

#-----------------
# Start of main program

#Register a signal handler
signal.signal ( signal.SIGHUP, catchSigInt )

# Start the main loop
doRepeatedMeasurements()

