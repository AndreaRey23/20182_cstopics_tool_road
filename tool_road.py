import numpy as np
import cv2
import collections
from functools import *
import Object as obj
import imutils
import objetdetect as classifier
import camrealSense as rs
import Esquinas as cn
import Interfaz as itf
import sys
import threading
import logging
import time



def Interface():
    global cap,cPlacas,app,ui
    app = itf.QApplication(sys.argv)
    ui = itf.mainwindow()
    print("Iniciando Interfaz")
    ui.setWindowTitle('Detector Placas')
    ui.show()
    sys.exit(app.exec_())
    cap.release()
    #realSense.stopCamera()
    cPlacas.realSense.stopCamera()
    print("Finalizando Interfaz")

def getBackground(img = []):

    # Apply background subtraction
    fgmask = fgbg.apply(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(gray.shape).astype('uint8')
    mask[fgmask>0] = 255
    #Dilatar con estructura de Cruz
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    mask = cv2.dilate(mask, kernel, iterations=4)
    #Erocionar con estructura de Elipse
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(4,4))
    mask = cv2.erode(mask, kernel, iterations=4)
    return mask

def getContourns(mask = []):

    color = 'G'
    num_Contornos = 20
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    # Get contours
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]  # Depende OpenCv
    center = None
    currentObjects = []
    # Check if contours were found (Solo primer contorno)

    if len(cnts) > 0 and len(cnts) < num_Contornos:
        # Find the biggest area contour
        # c = max(cnts, key=cv2.contourArea) #(Ultimo contorno
        C_Ordenados = sorted(cnts, key=cv2.contourArea)
        # Extract the circle that encloses the contour
        #print("Contornos",len(cnts))
        for idx, c in enumerate(C_Ordenados):
            if cv2.contourArea(c) > 60:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                #print(radius,idx)
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    #cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.rectangle(usrFrame,(int(x)-int(radius),int(y)-int(radius)),(int(x)+int(radius),int(y)+int(radius)),(198,140,120),2)
                    cv2.circle(usrFrame, (int(x), int(y)), 5, (128,128,255), -1)
                    #Ingresar Objeto
                    objeto = obj.object(idx, radius, center, color)
                    #print("Id",objeto.getId(),idx)
                    objeto.actualizar()
                    currentObjects.append(objeto)
    return currentObjects


def updateObjets():

    global currentObjects,trackingObjects,countObjects, cPlacas, ui
    #font = cv2.FONT_HERSHEY_SIMPLEX
    if len(currentObjects) > 0:
        #Buscar Bolas Nuevas y actualizar posicion bolas
        if not(len(trackingObjects)):
            #print("Objeto nuevo", len(currentObjects))
            for currentObject in currentObjects:
                trackingObjects.append(currentObject)
            #return(trackingObjects)

        for idx,currentObject in enumerate(currentObjects):
            new = 0
            for id,trackObject in enumerate(trackingObjects):
                pos = currentObject.getPosition()
                #print ("Pos " , idx, "=", pos)
                #print(trackObject.getId())
                if (trackObject.itsObject(pos,120)):
                    #trackObject = currentObject
                    #trackObject.Id = id
                    #trackObject.actualizar()
                    trackObject.Id = id
                    trackObject.setPosition(pos)
                    trackObject.actualizar()
                    #print(trackObject.getId(),trackObject.In)
                    trackObject.setRadio(currentObject.Radio)
                    trackObject.Color = currentObject.getColor()

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(usrFrame, str(trackObject.getId())+','+trackObject.getColor(), trackObject.getPosition(), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    new = 1
                    #print(trackObject.In)
                    #print ("Goal State : ",trackObject.Goalstate)
                    if trackObject.itsGoalstate(390):
                        countObjects += 1
                        print("Vehiculos Peaje : ",countObjects)
                        cv2.destroyAllWindows()

                        #Clasificador Placas
                        iter = 0
                        while True:
                            #ret, img = cPlacas.cap.read()
                            result = []
                            img = cPlacas.realSense.getFrame()
                            n = 10
                            # Show images
                            if len(img):
                                #img = imutils.resize(img , width = int(img.shape[1] * 1))
                                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                gray = cv2.equalizeHist(gray)
                                rects = cPlacas.detect(gray, cPlacas.cascade)
                                for p in rects:
                                    point = [[p[0],p[1]-n],[p[2],p[1]-n],[p[0],p[3]+n],[p[2],p[3]+n]]
                                    #print(point)
                                    #Correccion de Perspectiva
                                    correction = cn.perspectiveCorrection(img,point,dimensions=[500,300])

                                    #Encontrar Letras
                                    image = imutils.resize(correction, height = 300)
                                    bordes = cn.getBorders(image)

                                    points = cn.getCorners(bordes)
                                    centers = []
                                    try:
                                        centers = cn.orgPoints(points)
                                        correction = cn.perspectiveCorrection(image,centers)
                                        th = cn.plotAdapThreshold(cv2.cvtColor(correction, cv2.COLOR_BGR2GRAY), typ=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, size=27, C=2)
                                        # dilate 2 times
                                        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
                                        th = cv2.dilate(th, kernel, iterations=1)
                                        th = cv2.erode(th, kernel, iterations=1)
                                        result = cn.pytesseract.image_to_string(th)
                                        result = [x for x in result if((x >= "0" and x <= "9") or (x >= "A" and x <= "Z"))]
                                        print("Comprobando Placa",result)
                                        iter += 1
                                        #correction=imutils.resize(correction , width = int(correction.shape[1] * 0.2))
                                        ui.show_capture_placar(correction)
                                    except:
                                        print("Error Cuadro")
                                        continue
                                    #cv2.imshow("Placa", image)
                                    #cv2.imshow("Mask", th)
                                    #cv2.waitKey(0)
                                    #cv2.imshow('correction', correction)


                                cPlacas.draw_rects(img, rects, (0, 255, 0))
                                #cv2.imshow('objettect', img)
                                ui.show_capture_placa(img)

                            if iter > 6 and  len(result):
                                placa = result[:6]
                                ciudad = result[6:]
                                ui.write_txtCiudad("".join(ciudad))
                                ui.write_txtPlaca("".join(placa))

                                print("Placa Encontrada : ",placa," Ciudad : ",ciudad)
                                break


                        cv2.destroyAllWindows()
                    break

            if not(new):
                #print ("WIIII OBJETO NUEVA")
                #print(new,currentObjects[new].getPosition())
                trackingObjects.append(currentObject)
    return(trackingObjects)

def verMoveObject(frames):
    global trackingObjects
    # Calculate the elapsed time.
    if(frames  > 6):
        frames = 0
        for idx,trackObject in enumerate(trackingObjects):
            if (trackObject.Actualizaciones < 1):
                del(trackingObjects[idx-1])
                #print ("Eliminando",trackObject.Actualizaciones,trackObject.Id)
            else:

                #print ("Actualizando : ",trackBall.Actualizaciones,trackBall.Id)
                trackObject.setActualizaciones(0)

    return frames



app = 0
ui = 0
cap = cv2.VideoCapture(0)
#Clasificador
cascade_fn = "./trained_classifiers/cascadeHAAR_Jose.xml"
cPlacas = classifier.classifier(cascade_fn)

if __name__ == "__main__":

    d = threading.Thread(target=Interface, name='Interface')
    d.setDaemon(True)
    d.start()

    #Camara

    fgbg = cv2.createBackgroundSubtractorMOG2()
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus offe

    #Real Sense
    #realSense = rs.realSense()
    #realSense.initCamera()



    #cap.set(cv2.CAP_PROP_AUTO_EXPOSURE , 0.25)
    #cap.set(cv2.CAP_PROP_EXPOSURE, 10)
    trackingObjects = []
    countObjects = 0
    frames = 0

    while(True):

        currentObjects = []  # Bolas Actuales
    	# Capture frame and convert it to gray scale
        ret, frame = cap.read()
        usrFrame = frame
        mascara = getBackground(frame)
        foreground = cv2.bitwise_and(frame, frame, mask=mascara)
        currentObjects.extend(getContourns(mascara))


        frames += 1
        #print("Objetos Actuales",len(currentObjects))

        trackingObjects = updateObjets()
        frames = verMoveObject(frames)
        #print("Objetos Seguidos",len(trackingObjects))
        # Compute foreground (input masked)
        cv2.line(usrFrame, (0, 390), (640, 390), (0, 0, 255), 3)
        ui.show_capture_peaje(usrFrame)
        #cv2.imshow('frame',usrFrame)
        #cv2.imshow('mask',mascara)
        #cv2.imshow('foreground',foreground)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    #realSense.stopCamera()
    cPlacas.realSense.stopCamera()
    cv2.destroyAllWindows()
