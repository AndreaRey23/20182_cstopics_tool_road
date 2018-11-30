
# import the necessary packages
import imutils
#from skimage import exposure
import numpy as np
from matplotlib import pyplot as plt
import argparse
import cv2
import pytesseract
from PIL import Image
from pytesseract import image_to_string

def plotAdapThreshold(I, typ, size, C):
    th1 = cv2.adaptiveThreshold(I, 255, typ, cv2.THRESH_BINARY, size, C)
    #Erocionar con estructura de Elipse
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
    th1 = cv2.erode(th1, kernel, iterations=1)
    # plt.subplot(121)
    # plt.imshow(I, cmap = 'gray')
    # plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122)
    # plt.imshow(th1, cmap = 'gray')
    # plt.title('Thresholded Image'), plt.xticks([]), plt.yticks([])
    # plt.show()
    return th1


def orgPoints(centers = []):
    distance = 99999
    points1 = [centers[0],[0,0]]
    points2 = []
    orgCenters = [[0,0],[0,0],[0,0],[0,0]]
    for i in range(1,4):
        euclidian = abs(centers[0][0]-centers[i][0])+abs(centers[0][1]-centers[i][1])
        if(euclidian<distance):
            distance = euclidian
            points1[1] = centers[i]
    for i in range(1,4):
        if not(i == centers.index(points1[1])):
            points2.append(centers[i])
    #print("Points 1 : ", points1)
    #print("Points 2 : ", points2)
    c1=0;c2=1;
    if(points1[0][0] > points2[0][0]):
        c1 = 1;c2=0;

    if(points1[0][1]<points1[1][1]):
        orgCenters[0+c1] = points1[0]
        orgCenters[2+c1] = points1[1]
    else:
        orgCenters[2+c1] = points1[0]
        orgCenters[0+c1] = points1[1]

    if(points2[0][1]<points2[1][1]):
        orgCenters[0+c2] = points2[0]
        orgCenters[2+c2] = points2[1]
    else:
        orgCenters[2+c2] = points2[0]
        orgCenters[0+c2] = points2[1]

    return(orgCenters)

def getBorders(image = []):
    # load the query image, compute the ratio of the old height
    # to the new height, clone it, and resize it
    ratio = image.shape[0] / 300.0
    orig = image.copy()

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 60)
    # dilate 2 times
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    edged = cv2.dilate(edged, kernel, iterations=2)
    return  edged


def getCorners(edged = []):
    # Get contours
    _,cnts,_ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.054 * peri, True)
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            #print(approx)
            screenCnt = approx
            #print("Hola")
            break

    #a = cv2.drawContours(image, screenCnt, -1, (0, 255, 0), 3)
    #cv2.drawContours(image, [screenCnt], -1, (255, 0, 0), 3)
    #print(a)
    return [[x[0][0],x[0][1]] for x in approx]

def perspectiveCorrection(image = [],centers = [],dimensions = [700,400]):

    # Perspective Correction
    #pts1 = np.float32([[18,38],[217,58],[20,240],[217,254]]) # Esquina SuperiorI,Esquina SuperiorD,Esquina InferiorI,Esquina InferiorD
    pts1 = np.float32(centers)
    pts2 = np.float32([[0,0],[dimensions[0],0],[0,dimensions[1]],[dimensions[0],dimensions[1]]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(image,M,(dimensions[0],dimensions[1]))
    return dst


if __name__ == '__main__':

    # load the query image, compute the ratio of the old height
    # to the new height, clone it, and resize it
    image = cv2.imread('./Pruebas/H.png')
    image = imutils.resize(image, height = 300)
    bordes = getBorders(image)

    cv2.imshow("Game Boy Screen", bordes)
    cv2.waitKey(0)

    points = getCorners(bordes)
    centers = orgPoints(points)
    print(centers)

    cv2.imshow("Game Boy Screen", image)
    cv2.waitKey(0)

    correction = perspectiveCorrection(image,centers)
    th = plotAdapThreshold(cv2.cvtColor(correction, cv2.COLOR_BGR2GRAY), typ=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, size=57, C=2)
    result = pytesseract.image_to_string(th)
    print(result)

    cv2.imshow("Game Boy Screen", th)
    cv2.waitKey(0)
