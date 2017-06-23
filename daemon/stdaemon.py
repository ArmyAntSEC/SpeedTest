import subprocess
import json

proc = subprocess.Popen( './speedtest-cli --json', shell=True, stdout=subprocess.PIPE );

output = proc.communicate()

result = output[0]
print ( '-------' )
print ( result )
print ( '-------' )

#output = '{"bytes_sent": 2564096, "download": 10982638.579192186, "timestamp": "2017-06-23T19:51:42.012954Z", "share": null, "bytes_received": 13843204, "ping": 23.178, "upload": 1706722.617285763, "server": {"latency": 23.178, "name": "Kista", "url": "http://kst5-speedtest-1.tele2.net/speedtest/upload.php", "country": "Sweden", "lon": "17.9444", "cc": "SE", "host": "kst5-speedtest-1.tele2.net:8080", "sponsor": "Tele2", "url2": "http://kst5-speedtest-1.tele2.net/upload.php", "lat": "59.4014", "id": "6061", "d": 185.1072773722867}}'
jsonObj = json.loads(result)
print json.dumps( jsonObj, sort_keys=True, indent=4, separators=(',', ': '))

print ( '-------' )
print (  str(jsonObj['download']) + " / " + str(jsonObj['upload']) )
print ( '-------' )
print ( jsonObj['timestamp'])