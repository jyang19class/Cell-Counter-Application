import numpy as np
import cv2


def countCells(x, y, imagePath, saturation, hueRange):
    #load color image
    img = cv2.imread(imagePath, 1)
    original = img.copy()
    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((3,3),np.uint8)
    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    kernel4 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

    # \convert to HSV
    blur = cv2.GaussianBlur(img, (3,3), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Find HSV value at point
    hsvColor = hsv[y,x]

    #Define Ranges for HSV threshold
    print(hsvColor[0])
    lowerRange = np.array([hsvColor[0]-int(hueRange), int(saturation), 80])
    upperRange = np.array([hsvColor[0]+int(hueRange), 255, 255])

    #create mask
    mask = cv2.inRange(hsv, lowerRange, upperRange)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel3)

    #bitwise and mask and original image
    result = cv2.bitwise_and(original, original, mask=mask)
    inverseMask = cv2.bitwise_not(mask)
    inverseMask = cv2.cvtColor(inverseMask, cv2.COLOR_GRAY2BGR)
    result = cv2.add(result, inverseMask)

    #Otsus Binarization
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(result,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel3)

    #Sure Background Area
    sure_bg = cv2.dilate(thresh, kernel2, iterations=2)

    #Sure Foreground Area
    sure_fg = cv2.erode(thresh, kernel4, iterations=2)

    #Find Unknown Region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    #Seperate Unknown Region
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers+1
    markers[unknown==255] = 0

    #Watershed
    markers = cv2.watershed(img, markers)
    img[markers==-1] = [0,0,255]
    print(len(np.unique(markers))-2)
    b,g,r = cv2.split(img)
    img = cv2.merge((r,g,b))
    return img
