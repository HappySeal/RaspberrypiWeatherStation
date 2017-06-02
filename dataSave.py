import Adafruit_DHT as DHT
import os , time,sqlite3
import Adafruit_BMP.BMP085 as BMP180
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)
con = sqlite3.connect("RaspAir.db")
cursor = con.cursor()
def table():
        cursor.execute("CREATE TABLE IF NOT EXISTS Hava_Durumu (tarih TEXT, sic FLOAT , nem FLOAT,basinc FLOAT)")
def hourMinute():
        return ((int(time.strftime("%H")))*60+int(time.strftime("%M")))
def Now():
        str(time.strftime("%Y")) + "/" + str(time.strftime("%m")) + "/" + str(time.strftime("%d")) + "_" + str(time.strftime("%H")) + ":" + str(time.strftime("%M"))
table()
now = hourMinute()
while True:
        sensor = BMP180.BMP085()
        nem,sic = DHT.read_retry(11,4)
        if  hourMinute() - now == 5:
                now = hourMinute()
                cursor.execute("INSERT INTO Hava_Durumu (tarih,sic,nem,basinc) VALUES (?,?,?,?)",(Now(),sic,nem,(sensor.read_pressure()/100)))
        else:
                print("En son kayitdan gecen sure {0} dakika".format(((int(time.strftime("%H")))*60+int(time.strftime("%M")))-now))
                print("Sicaklik BMP : {0:0.2f} *C".format(sensor.read_temperature()))
                print("Basinc BMP : {0:0.2f} Pa".format(sensor.read_pressure()))
                print("Rakim BMP : {0:02f} m".format(sensor.read_altitude()))
                print("Deniz Seviyesi Basinci BMP : {0} mB".format(sensor.read_sealevel_pressure()))
                print("Sicaklik DHT : {0}".format(sic))
                print("Nem DHT : {0}".format(nem))


        time.sleep(1)
        os.system("clear")
        if(GPIO.input(17)):
                con.close()
                quit()
