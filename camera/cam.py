from picamera2 import Picamera2, Preview
from picamera2.encoders import Encoder
import numpy as np

import os
import glob
import time
import cv2 
from cv2 import imwrite

class CamClass:
    cnt = 0
    ndarrType = type(np.array([]))
    displayName = '_'
    size = (640, 480)
    path = os.path.abspath('.') + '/img/'

    def __init__(self, visROI=True):
        self.clean()
        self.visROI = visROI
        self.__setROI__([(0,0), self.size])
        
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": self.size}))
        self.picam2.start()

        self.img = None

    
    def run(self):
        while True:
            self.img01 = self.picam2.capture_array() 
            self.img02 = self.picam2.capture_array()  
            self.img03 = self.picam2.capture_array() 
            self.detectMotion()
            
            if self.visROI:
                self.visualizeROI()
                
            # self.calcDiff()
            cv2.imshow(self.displayName, self.img03)
            
            
            key = cv2.waitKey(30)
            if key == ord('q'):
                break
            elif key == ord('c'):
                self.cap()
            elif key == ord('s'):
                self.setROI()
    
    
    def visualizeROI(self):
        cv2.rectangle(self.img03, self.ROI[0], self.ROI[1], (0,255,0), 3)  
            
    def cap(self, ROI=False):
        if ROI:
            imwrite(self.path+time.asctime()+'.png', self.__getCapROI(self.img02))
        else:
            imwrite(self.path+time.asctime()+'.png', self.img02)
    

    def clean(self):
        [os.remove(file) for file in glob.glob(self.path + '*.png')]
        
    def setROI(self):
        roi = []
        def mouse_event(event, x, y, flags, param):
            if event == cv2.EVENT_FLAG_LBUTTON:
                cv2.circle(self.img03, (x, y), 5, (0, 0, 250), -1)
                roi.append((x,y))
                cv2.imshow(self.displayName, self.img03)
                
                
        def check():
            if len(roi) != 2:
                return False
            roi.sort()
            
            print(roi)
            cv2.waitKey()
            return roi[0][0] < roi[1][0] and roi[0][1] < roi[1][1]
        
        while len(roi) < 2:
            cv2.setMouseCallback(self.displayName, mouse_event, self.img03)
            if len(roi) > 2 or cv2.waitKey(20) ==ord('q'):
                break
        
        if check() == False:
            print("invalid ROI")
            return
        
        self.__setROI__(roi)
        
    def __setROI__(self, roi):
        self.ROI = roi
        self.ROIh= abs(self.ROI[1][1] - self.ROI[0][1])
        self.ROIw= abs(self.ROI[1][0] - self.ROI[0][0])
        self.ROISize = self.ROIh * self.ROIw
    
    def __getROI__(self, img):
        return img[self.ROI[0][1] : self.ROI[1][1], self.ROI[0][0] : self.ROI[1][0]]
    
    def __getCapROI(self, img):
        return img[
            self.ROI[0][1]-10 if self.ROI[0][1]-10 >=0 else 0 : \
            self.ROI[1][1]+10 if self.ROI[1][1]+10 <= self.size[1] else self.size[1], \
            self.ROI[0][0]-10 if self.ROI[0][0]-10 >=0 else 0 : \
            self.ROI[1][0]+10 if self.ROI[1][0]+10 <= self.size[0] else self.size[0]]

    def detectMotion(self):
        def Gaussian(img):
            return cv2.GaussianBlur(img, (0,0), 3)
        
        gray_img01 = cv2.cvtColor(Gaussian(self.__getROI__(self.img01)), cv2.COLOR_BGR2GRAY)
        gray_img02 = cv2.cvtColor(Gaussian(self.__getROI__(self.img02)), cv2.COLOR_BGR2GRAY)
        gray_img03 = cv2.cvtColor(Gaussian(self.__getROI__(self.img03)), cv2.COLOR_BGR2GRAY)
        
        difference_01 = cv2.absdiff(gray_img01, gray_img02)
        difference_02 = cv2.absdiff(gray_img02, gray_img03)
        
        _, difference_01 = cv2.threshold(difference_01, 20, 255, cv2.THRESH_BINARY)
        _, difference_02 = cv2.threshold(difference_02, 20, 255, cv2.THRESH_BINARY)

        diff = cv2.bitwise_and(difference_01, difference_02)   
        diff_cnt = cv2.countNonZero(diff) 
    
        cv2.imshow("Motion Sensing", diff)

        print(diff_cnt)
        
        if diff_cnt>50:
            if self.cnt >= 3:
                self.cap(ROI=True)
                self.cnt = 0

            self.cnt+=1
        else:
            self.cnt = 0
    
cam = CamClass()

def makeCamInstance(vis=True):
    cam = CamClass(vis)
    return cam
    
def getCam():
    return cam    

def runCam():
    cam.run()