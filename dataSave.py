import Adafruit_DHT as DHT
import os , time,sqlite3
import Adafruit_BMP.BMP085 as BMP180
import Rpi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO)
con = sqlite.connect("RaspAir.db")
cursor = con.cursor()
def table():
        cursor.execute("CREATE TABLE IF NOT EXISTS Hava_Durumu (yil INT,ay INT,gun INT,saat INT ,dakika INT , sic FLOAT , nem FLOAT,basinc FLOAT)")
def hourMinute():
        return ((int(time.strftime("%H")))*60+int(time.strftime("%M")))
table()
now = hourMinute()
while True:
        sensor = BMP180.BMP085()
        nem,sic = DHT.read_retry(11,4)
        if  hourMinute() - now == 10:
                now = hourMinute()
                cursor.execute("INSERT INTO Hava_Durumu (yil,ay,gun,saat,dakika,sic,nem,basinc) VALUES (?,?,?,?,?,?,?,?)",(int(time.strftime("%Y"))),int(time.strftime("%m")),int(time.strftime("%H")),int(time.strftime("%M")),sic,nem,sensor.read_pressure())
        else:
                print(((int(time.strftime("%H")))*60+int(time.strftime("%M")))-now)
                print("Sicaklik BMP : {0:0.2f} *C".format(sensor.read_temperature()))
                print("Basinc BMP : {0:0.2f} Pa".format(sensor.read_pressure()))
                print("Rakim BMP : {0:02f} m".format(sensor.read_altitude()))
                print("Deniz Seviyesi Basinci BMP : {0:0.2f} Pa".format(sensor.read_sealevel_pressure()))
                print("Sicaklik DHT : {0}".format(sic))
                print("Nem DHT : {0}".format(nem))



        if(GPIO.input(17)):
                con.close()
                quit()
