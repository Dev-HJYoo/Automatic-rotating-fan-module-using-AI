######## Webcam Capture program #########
#
# Author: Yoo Hyeong Jun
# Date: 6/18/19
# Description: 
# Capture 100 times image for webcam

import cv2
import time
import threading

global image # Global image variable
def execute(): # Define Thread object
    count = 0
    while(count < 100): # Capture 100 times
        print('Saved frame number : ' + str(int(cap.get(0))))
        cv2.imwrite("images\l%d.jpg" % count, image)
        print('Saved framea%d.jpg' % count)
        count += 1
        if count == maxs:
            break
        time.sleep(1)
    

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print("unable to read camera feed")

while 1: # Check Webcam

    
    ret, image = cap.read()
    

    cv2.imshow("ffff", image)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

my_thread = threading.Thread(target = execute) # Define Thread
my_thread.start()     # Start Thread

while(True):
    ret, image = cap.read()
    cv2.imshow("sss",image)
    if cv2.waitKey(0) == 'k': # Press k to exit
        break
    
cap.release()
cv2.destroyAllWindows()


