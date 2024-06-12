
import serial
import pymysql
#connect to database
dbConn = pymysql.connect("localhost","thinhd464","","temperature_db")or die("no connection")
#crette cursor
cursor = dbConn.cursor()
ser = serial.Serial('/dev/ttyS0',9600)
led1_on = False
led2_on = False

while True:
	temp = ser.readline().decode('utf-8').rstrip('\r\n')
	light =ser.readline().decode('utf-8').rstrip('\r\n')
	
	print ("temp: {} C, Light: {} lux".format(temp, light))
	
	#inserdata to table
	cursor.execute("INSERT INTO sensordata (temperature,light) VALUES(%s, %s)",(temp,light))
	#dbConn.commit()
	#cursor.close()
	
	if float(temp) > 24 or float(temp) < 15:
		ser.write(b'2')
		print("Temp threshold exceeded")
		led2_on = True
	else:
		if led2_on:
			ser.write(b'5')

			led2_on = False
	
	if float(light) > 400 or float(light) < 40:
		ser.write(b'1')
		print("Light threshold exceeded")
		led1_on = True
	else:
		if led1_on:
			ser.write(b'4')

			led1_on = False
	if led1_on and led2_on:
		ser.write(b'3')

	else:
		ser.write(b'6')
	#update led status on mysql
	if led1_on and led2_on:
		led_on = "both"
	elif led1_on:
		led_on = "light"
	elif led2_on:
		led_on = "temp"
	else:
		led_on = None
	
	cursor.execute("Update sensordata SET led_on = %s WHERE id = (SELECT MAX(id) FROM sensordata)",(led_on,))
	dbConn.commit()
		
	
	
	
		
