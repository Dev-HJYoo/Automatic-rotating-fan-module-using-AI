######## Client ( Raspberry Pi ) Code #########
#
# Author: Yoo Hyeong Jun
# Date: 6/18/19
# Description: 
# This program uses Motor code and Socket transport code
# It captures image from webcam.
# it sends image to server via socket transport.
# It receive state information from server via socket transport.
# It use convert image to jpg.
# It use convert numpy array to string.
# Using Socket Transport
# Transport Presentence ( Left - 1, Right - 2, Rotation - 3 )

## Some of the code is copied from Motor Control at
## https://m.blog.naver.com/chandong83/221156273595

## Some of the code is copied from Socket Transport at
## https://brownbears.tistory.com/207

## but I changed it to make it more understandable and usable to me




# import 
import cv2
import socket
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
import threading


##### Motor
STOP  = 0
FORWARD  = 1
BACKWARD = 2
# motor channel
CH1 = 0
CH2 = 1
# PIN io set
OUTPUT = 1
INPUT = 0
# PIN set
HIGH = 1
LOW = 0
# pin define
#PWM PIN
ENA = 26  #37 pin
#GPIO PIN
IN1 = 19  #35 pin
IN2 = 13  #33 pin

# pin set func
def setPinConfig(EN, INA, INB):        
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    # 100khz PWM run 
    pwm = GPIO.PWM(EN, 1) 
    # PWM stop for run   
    pwm.start(0) 
    return pwm

# motor control func
def setMotorContorl(pwm, IN1, IN2, speed, stat):
    # motor speed control PWM
    pwm.ChangeDutyCycle(speed)  
    count = 0
    if stat == FORWARD:
        GPIO.output(IN1, 0)
        while True: 
            GPIO.output(IN2, 0) 

            GPIO.output(IN2, 1)
            #setMotor(CH1, 50, FORWARD)
            count+=1
            if count==500:
                break
    elif stat == BACKWARD:
        GPIO.output(IN1, 1)
        while True: 
            GPIO.output(IN2, 0) 

            GPIO.output(IN2, 1)
            #setMotor(CH1, 50, FORWARD)
            count+=1
            if count==500:
                break
            
# rapping func for run easy
def setMotor(ch, speed, stat):
    if ch == CH1:
        #pwmA set get pwm handdle
        setMotorContorl(pwmA, IN1, IN2, speed, stat)  

# Thread Func	
def execute():
    # state is global
    global state

    # Motor init
    count = 0
    GPIO.setmode(GPIO.BCM)
    pwmA = setPinConfig(ENA, IN1, IN2)
    pwmA.ChangeDutyCycle(50)

    # Motor Control
    while True:
        print(state)

        # Left
        if state == 1:
            GPIO.output(IN1, 0)
            while True: 
                GPIO.output(IN2, 0) 
                sleep(0.01)
                GPIO.output(IN2, 1)
                #setMotor(CH1, 50, FORWARD)
                count+=1
                if count==2:
                    count = 0
                    break

        # Right
        elif state == 2:
            GPIO.output(IN1, 1)
            while True: 
                GPIO.output(IN2, 0) 
                sleep(0.01)
                GPIO.output(IN2, 1)
                #setMotor(CH1, 50, FORWARD)
                count+=1
                if count==2:
                    count = 0
                    break
                
        # Rotation
        else: 
            while True: 
                GPIO.output(IN2, 0) 
                sleep(0.01)
                GPIO.output(IN2, 1)
                #setMotor(CH1, 50, FORWARD)
                count+=1
                if count==2:
                    count = 0
                    break

            

# Receive Func
def recvall(sock, count):
    # Byte String
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('PC_IP', 8485))

cam = cv2.VideoCapture(0)


d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
d.bind(('Raspberry_IP',8486))
d.listen(10)
donn, addr = d.accept()

# encode parameter
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

my_thread = threading.Thread(target = execute) # Define Thread
my_thread.start()     # Start Thread

# state = 3
state = 3

while True:

	# Capture image from webcam
	ret, frame = cam.read()

	# view webcam
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) == ord('q'):
	    break

	# convert to jpg
	result, frame = cv2.imencode('.jpg', frame, encode_param)

	# numpy array of image
	data = np.array(frame)

	# convert string
	stringData = data.tostring()

	# Send 16byte( string length ) and string data
	s.sendall((str(len(stringData))).encode().ljust(16) + stringData)

        # receive state string
	rev = int(recvall(donn,1).decode('utf-8'))
	
	state = rev
				
	
cam.release()
