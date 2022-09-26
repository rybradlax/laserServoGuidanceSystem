from threading import Thread
import numpy as np
import time
import cv2


class TargetingThread:
    
    def __init__(self):
        resolution = (1280,720)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0]) 
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.frame = None
        self.ret = None
        self.stopped = False


    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while self.cap.isOpened():
                self.ret,self.frame = self.cap.read()
                if self.ret == False:
                    self.stopped = True
                if self.stopped:
                        self.cap.release()
                        cv2.destroyAllWindows()
                        return

    def start2(self):
        Thread(target=self.write, args=()).start()
        return self

                    
    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
