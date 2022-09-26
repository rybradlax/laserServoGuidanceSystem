import cv2
import numpy as np
from arduinoUtils import transmitData
import time
import serial
import struct

ser = serial.Serial('COM4', 115200, timeout = 0.2)

def contour(cts):
    rect = cv2.minAreaRect(cts)
    box = cv2.boxPoints(rect)
    return(np.int0(box),rect)

def angleProperties(pixCount):
    theta = 0.09375*pixCount
    return theta
def findMax(x):
    idx = 0
    max = 0
    for i,y in enumerate(x):
        if y > max:
            max = y
            idx = i
    return idx,max

cap = cv2.VideoCapture(0)


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

lowL = [0,0,0]
highL = [123,123,13]
low=np.array(lowL)
high=np.array(highL)
try:
    low1 = int(input("Input low value 1"))
    low2 = int(input("Input low value 2"))
    low3 = int(input("Input low value 3"))
    high1 = int(input("Input high value 1"))
    high2 = int(input("Input high value 2"))
    high3 = int(input("Input high value 3"))
    lowL[0] = low1
    lowL[1] = low2
    lowL[2] = low3
    highL[0] = high1
    highL[1] = high2
    highL[2] = high3
    low=np.array(lowL)
    high=np.array(highL)
except Exception as e:
            print(e)
            print("Make sure to input integers")
            pass

right = False
left = False
center = False
turn = "None"

while True:
    ret,frame = cap.read()
    if ret == False:
        break

    mask = cv2.inRange(frame, low, high)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # Find the contours of the mask
    cnts = list(cnts)
    areaList = []
    thetaList = []
    turnList = []
    temp = 0
    if len(cnts)!=0:
        for i,cts in enumerate(cnts):
            boxd,rect = contour(cts)

            end = len(cnts)-1
            
            area1 = list(rect)
            area = area1[1][0]*area1[1][1]
            xCoord = area1[0][0]
            
            if area > 20:
                areaList.append(area) 
                if xCoord > 630 and xCoord < 650:
                    center = True
                    left = False
                    right = False
                    turn = "Center"
                elif xCoord < 630:
                    left = True
                    right = False
                    center = False
                    turn = "Left"
                elif xCoord > 650:
                    right = True
                    left = False
                    right = False
                    turn = "Right"
##                if 640 > xCoord:
##                    pixDist = 640-xCoord
##                else:
##                    pixDist = xCoord-640
                turnList.append(turn)
                pixDist = 640-xCoord
                theta = angleProperties(pixDist)
                if theta < 0:
                    theta = abs(theta)
                    theta = 90-theta
                else:
                    theta = 90+theta
                thetaList.append(theta)
                    
                cv2.drawContours(mask,[boxd.astype(int)],0,(56,74,54),2)
                cv2.drawContours(frame,[boxd.astype(int)],0,(56,74,54),2)
                   # if not center:
                    #    transmitData.send(int(round(theta,0)))
                     #   print("Data sent")
                      #  time.sleep(0.5)
    idx,max = findMax(areaList)
    if len(thetaList)>0:
         if turnList[idx]=='Center':
              print("Center")
         else:
              #line = transmitData.send(int(round(thetaList[idx],0)))
              ser.write(int(round(theta,0)))  
              print(int(round(theta,0)))
            #  if(line == thetaList[idx]):
             #      print(int(round(thetaList[idx],0)))
              #     time.sleep(.2) 
              #else:
               #    print("intLine not = theta: "+str(line))
         if True:
                        screenText = 'Angle= ' + str(round(thetaList[idx],0)) + ' Turn: '+turnList[idx]
                        cv2.line(frame,(610,360),(670,360),(255,0,0),2) #draw line in middle of screen
                        cv2.line(frame,(640,330),(640,390),(255,0,0),2) #draw line in middle of screen
                        font                   = cv2.FONT_HERSHEY_SIMPLEX
                        bottomLeftCornerOfText = (850,360)
                        fontScale              = 1
                        fontColor              = (255,255,255)
                        lineType               = 2
                        cv2.putText(frame, screenText, 
                        bottomLeftCornerOfText, 
                        font, 
                        fontScale,
                        fontColor,
                        lineType)
    cv2.imshow("Frame",frame)
    cv2.imshow("Mask",mask)

    
    
    if cv2.waitKey() & 0xFF == ord('q'):
        try:
            low1 = int(input("Input low value 1"))
            low2 = int(input("Input low value 2"))
            low3 = int(input("Input low value 3"))
            high1 = int(input("Input high value 1"))
            high2 = int(input("Input high value 2"))
            high3 = int(input("Input high value 3"))
            lowL[0] = low1
            lowL[1] = low2
            lowL[2] = low3
            highL[0] = high1
            highL[1] = high2
            highL[2] = high3
            low=np.array(lowL)
            high=np.array(highL)
        except Exception as e:
            print(e)
            print("Make sure to input integers")
            pass
    elif cv2.waitKey() & 0xFF == ord('k'):
        cap.release()
        cv2.destroyAllWindows()
        break

        
        
cap.release()
cv2.destroyAllWindows()
        
