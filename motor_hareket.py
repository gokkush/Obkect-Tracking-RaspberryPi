import RPi.GPIO as GPIO
import time


sagileri=12
saggeri=26
solileri=19
solgeri=13
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sagileri, GPIO.OUT)
GPIO.setup(saggeri, GPIO.OUT)
GPIO.setup(solileri, GPIO.OUT)
GPIO.setup(solgeri, GPIO.OUT)
GPIO.output(sagileri , 0)
GPIO.output(saggeri , 0)
GPIO.output(solileri, 0)
GPIO.output(solgeri, 0)

def soladon():
    print ("SOLA DÖN")
    GPIO.output(solileri , 0)
    GPIO.output(solgeri , 0)
    GPIO.output(sagileri , 1)
    GPIO.output(saggeri , 0)

def sagadon():
   print ("SAĞA DÖN")
    GPIO.output(solileri , 1)
    GPIO.output(solgeri , 0)
    GPIO.output(sagileri , 0)
    GPIO.output(saggeri , 0)

def ileri():
   print ("İLERİ GİT")
   GPIO.output(sagileri , 1)
   GPIO.output(saggeri , 0)
   GPIO.output(solileri , 1)
   GPIO.output(solgeri , 0)


def geri():
   print ("GERİ GİT")
   GPIO.output(sagileri , 0)
   GPIO.output(saggeri , 1)
   GPIO.output(solileri , 0)
   GPIO.output(solgeri , 1)

def dur():
   print ("DUR")
   GPIO.output(sagileri , 0)
   GPIO.output(saggeri , 0)
   GPIO.output(solileri , 0)
   GPIO.output(solgeri , 0)
 
data=""
try:
    while True:

        ileri()
		time.sleep(2)
		geri()
		time.sleep(2)
		sagadon()
		time.sleep(2)
		soladon()
		time.sleep(2)
		dur()
		time.sleep(2)
        break
        
except IOError:
    pass

GPIO.cleanup()
