import cv2
import numpy as np
from arduinoUtils import transmitData
from TargetingThread import TargetingThread as tt
import time

def contour(cts):
    rect = cv2.minAreaRect(cts)
    box = cv2.boxPoints(rect)
    return(np.int0(box),rect)

def angleProperties(pixCount):
    theta = 0.09375*pixCount
    return theta

t = tt().start()



#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) 
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

lowL = [0,0,0]
highL = [45,67,29]
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
thetaList = []
turnList = []
while True:
    frame = t.read()
    #if frame == None:
      #  print("bad frame")
     #   break
    #ret,frame = cap.read()
    #if ret == False:
     #   break

    mask = cv2.inRange(frame, low, high)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # Find the contours of the mask
    cnts = list(cnts)

    if len(cnts)!=0:
        for i,cts in enumerate(cnts):
            boxd,rect = contour(cts)

            end = len(cnts)-1
            
            area1 = list(rect)
            area = area1[1][0]*area1[1][1]
            xCoord = area1[0][0]
            
            if area > 1000:
                cv2.drawContours(mask,[boxd.astype(int)],0,(56,74,54),2)
                cv2.drawContours(frame,[boxd.astype(int)],0,(56,74,54),2)
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
                pixDist = 640-xCoord
                theta = angleProperties(pixDist)
                if theta < 0:
                    theta = abs(theta)
                    theta = 90-theta
                else:
                    theta = 90+theta
                thetaList.append(theta)
                turnList.append(turn)
                if i == end:
                    if True:
                        screenText = 'Angle= ' + str(round(theta,1)) + ' Turn: '+turn
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
                        lineType)### Put text on the screen
                    
                    
##                    if not center or center:
##                        transmitData.send(int(round(theta,0)))
##                        print(int(round(theta,0)))
##                        print("Data sent")
##                        time.sleep(1)
    temp = -100.0
    for idx,f in enumerate(thetaList):
        print("here")
        #if thetaList[idx] <= temp+5.0 and thetaList[idx] >= temp-5.0:
        if turnList[idx] != "Center":
            transmitData.send(int(round(thetaList[idx],0)))
            print(int(round(theta)))
            time.sleep(0.5)
            temp = thetaList[idx]
    thetaList = []
    turnList = []
        
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
        t.stop()
        break
        

        
cv2.destroyAllWindows()
        
