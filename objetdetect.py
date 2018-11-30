#!/usr/bin/env python

import numpy as np
import cv2
import imutils
import camrealSense as rs



class classifier:

    def __init__(self,cascade_fn):

        #self.cap = cv2.VideoCapture(1)
        self.cascade = cv2.CascadeClassifier(cascade_fn)
        #Real Sense
        self.realSense = rs.realSense()
        self.realSense.initCamera()


    def detect(self, img, cascade):
        #rects = cascade.detectMultiScale(img, scaleFactor=1.1128, minNeighbors=14, minSize=(120, 80), flags = cv2.CASCADE_SCALE_IMAGE) # Clasificador LBP CATA 3
        #rects = cascade.detectMultiScale(img, scaleFactor=1.1008, minNeighbors=8, minSize=(40, 20), flags = cv2.CASCADE_SCALE_IMAGE) # Clasificador HAAR CATA 2
        rects = cascade.detectMultiScale(img, scaleFactor=1.0878, minNeighbors=8, minSize=(60, 60), flags = cv2.CASCADE_SCALE_IMAGE) # Clasificador HAAR JOSE 1
        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        return rects

    def draw_rects(self, img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)




if __name__ == '__main__':

    cascade_fn = "./trained_classifiers/cascadeHAAR_Jose.xml"

    cPlacas = classifier(cascade_fn)
    num = 0
    while True:

        #ret, img = cPlacas.cap.read()
        img = cPlacas.realSense.getFrame()
        # Show images
        if len(img):
            #img = imutils.resize(img , width = int(img.shape[1] * 1))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            rects = cPlacas.detect(gray, cPlacas.cascade)
            cPlacas.draw_rects(img, rects, (0, 255, 0))
            cv2.imshow('objettect', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cPlacas.realSense.stopCamera()
    cv2.destroyAllWindows()
