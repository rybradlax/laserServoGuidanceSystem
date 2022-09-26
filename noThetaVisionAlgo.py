import cv2
import numpy as np
from arduinoUtils import transmitData
import time

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
    xCoordList = []
    boxdList = []
    temp = 0

    if len(cnts)!=0:
        for i,cts in enumerate(cnts):
            boxd,rect = contour(cts)
            boxdList.append(boxd)
            end = len(cnts)-1
            
            area1 = list(rect)
            area = area1[1][0]*area1[1][1]
            xCoord = area1[0][0]

            areaList.append(area)
            xCoordList.append(xCoord)
            
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
                turnList.append(turn)
        if len(areaList)>0:
            idx,max = findMax(areaList)
            if turnList[idx] == 'Right':
                if 1280 - xCoordList[idx] > 300:
                    transmitData.send2('m') # 10 degrees
                elif 1280-xCoordList[idx]>100 and 1280-xCoordList[idx]<300:
                    transmitData.send2('n') # 5 degrees
                elif 1280-xCoordList[idx]<100:
                    transmitData.send2('b') # 3 degrees
                elif 1280-xCoordList[idx]<50:
                    transmitData.send2('v') # 1 degree
            elif turnList[idx] == 'Left':
                if xCoordList[idx] - 1280 > 300:
                    transmitData.send2('c') # 10 degrees
                elif xCoordList[idx] - 1280>100 and xCoordList[idx] - 1280<300:
                    transmitData.send2('x') # 5 degrees
                elif xCoordList[idx] - 1280<100:
                    transmitData.send2('z') # 3 degrees
                elif xCoordList[idx] - 1280<50:
                    transmitData.send2('l') # 1 degree
            else:
                pass
            if True:
                        screenText = 'Moving '+turnList[idx]
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
            cv2.drawContours(frame,[boxdList[idx].astype(int)],0,(255,0,0),2)
            cv2.imshow("Frame",frame)

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
        

            
