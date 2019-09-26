
from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO

#motorların GPIO numaralarını tanıtıyoruz
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


def positionxkonumu (xkonumu, angle):
    #os.system("python anglexkonumuCtrl.py " + str(xkonumu) + " " + str(angle))
    print("X konumu: {0}, Y Konumu: {1} \n".format(xkonumu, angle))


def konumOgren (x, y):
    global panangle
    global tiltangle
    if (x < 220):
        GPIO.output(sagileri, GPIO.LOW)
        GPIO.output(saggeri, GPIO.LOW)
        GPIO.output(solileri, GPIO.HIGH)
        GPIO.output(solgeri, GPIO.LOW)
        time.sleep(.05)
        GPIO.output(sagileri, GPIO.LOW)
        GPIO.output(saggeri, GPIO.LOW)
        GPIO.output(solileri, GPIO.LOW)
        GPIO.output(solgeri, GPIO.LOW)
        print("Sağa Dönüyor..")
        positionxkonumu (x, y)
 
    elif (x > 280):
        GPIO.output(sagileri, GPIO.HIGH)
        GPIO.output(saggeri, GPIO.LOW)
        GPIO.output(solileri, GPIO.LOW)
        GPIO.output(solgeri, GPIO.LOW)
        time.sleep(.05)
        GPIO.output(sagileri, GPIO.LOW)
        GPIO.output(saggeri, GPIO.LOW)
        GPIO.output(solileri, GPIO.LOW)
        GPIO.output(solgeri, GPIO.LOW)
        print("Sola Dönüyor..")
        positionxkonumu (x, y)

    elif (y < 60):
        GPIO.output(sagileri, GPIO.HIGH)
        GPIO.output(saggeri, GPIO.LOW)
        GPIO.output(solileri, GPIO.HIGH)
        GPIO.output(solgeri, GPIO.LOW)
        time.sleep(.06)
        GPIO.output(sagileri, GPIO.LOW)
        GPIO.output(saggeri, GPIO.LOW)
        GPIO.output(solileri, GPIO.LOW)
        GPIO.output(solgeri, GPIO.LOW)
        print("İleri Gidiyor..")
        positionxkonumu (x, y)
        
    elif (y > 60):
        GPIO.output(sagileri, GPIO.HIGH)
        GPIO.output(saggeri, GPIO.LOW)
        GPIO.output(solileri, GPIO.HIGH)
        GPIO.output(solgeri, GPIO.LOW)
        positionxkonumu (x, y)
    else:
        GPIO.output(sagileri, GPIO.LOW)
        GPIO.output(saggeri, GPIO.LOW)
        GPIO.output(solileri, GPIO.LOW)
        GPIO.output(solgeri, GPIO.LOW)
        print("Durduruldu..")

print("Kamera Isınıyor. Lütfen bekleyiniz...")
vs = VideoStream(0).start()
time.sleep(1.0)

# tanıttığımız nesnenin üst ve alt renk aralıkları belirleniyor.
colorLower = (167, 100, 100)
colorUpper = (197, 255, 255)

# video çekimini sürekli hale getiriyor ve yer tespiti yapıyoruz
while True:
        # alınan video görüntüsünü hsv formatına dönüştürüp böylece sadece bir rengi görmesini sağlıyoruz
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	frame = imutils.rotate(frame, angle=360)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# maskeleme işlemi yopıyoruz
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

        # maskelediğimiz nesnenin x ve y koordinatlarını bulup, merkezini belirliyoruz.
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None
	if len(cnts) == 0:
            print("Nesne tespit edilemedi.")
            #GPIO.output(sagileri, GPIO.HIGH)
            #GPIO.output(saggeri, GPIO.LOW)
            #GPIO.output(solileri, GPIO.LOW)
            #GPIO.output(solgeri, GPIO.HIGH)
            #time.sleep(.05)
            GPIO.output(sagileri, GPIO.LOW)
            GPIO.output(saggeri, GPIO.LOW)
            GPIO.output(solileri, GPIO.LOW)
            GPIO.output(solgeri, GPIO.LOW)
            
	# Eğer nesne kameraya görünürse
	elif len(cnts) > 0:
		# maskelediğimiz video görüntüsündeki çemberin ne kadar büyük olması gerektiğini bulmak için rengin maksimum büyüklüğünü algılatıyoruz
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		
		if radius > 10:
                # çevreleyen daireyi ve daire merkezini belirleyip hareketi algılatıyoruz
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			
			# konumu yazdırıyoruz
			konumOgren(int(x), int(y))
			

	# # video görüntüsünü ekrana veriyoruz
	cv2.imshow("Nesne Takip: M.G, S.P, E.U, N.K, M.C.K", frame)
	
	# ESC tuluna basılınca programdan çıkıyor
	key = cv2.waitKey(1) & 0xFF
	if key == 27:
            vs.stop()
            cv2.destroyAllWindows()
            print("\n Programdan çıkılıyor...  \n Bellek temizleniyor...")
            GPIO.cleanup()
            time.sleep(0.5)
            break


