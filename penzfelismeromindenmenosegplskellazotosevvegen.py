import cv2
import numpy as np

def haboskecsaposturmux(x):
    pass

def apro(): 
    x = 0
    #nyissa meg a jobb oldali kaput 
    #zárja be a bal oldali kaput
def bankjegy():
    x= 0
    #nyissa meg a bal oldali kaput 
    #zárja be a jobb oldali kaput

cam = cv2.VideoCapture(0)

cv2.namedWindow("csuszka")
cv2.createTrackbar('L-H', 'csuszka', 0, 180,haboskecsaposturmux)
cv2.createTrackbar('L-S', 'csuszka', 0, 255,haboskecsaposturmux)
cv2.createTrackbar('L-V', 'csuszka', 97, 255,haboskecsaposturmux)
cv2.createTrackbar('U-H', 'csuszka', 180, 180,haboskecsaposturmux)
cv2.createTrackbar('U-S', 'csuszka', 255, 255,haboskecsaposturmux)
cv2.createTrackbar('U-V', 'csuszka', 255, 255,haboskecsaposturmux)

betutipus = cv2.FONT_HERSHEY_DUPLEX 


while True:
    _, kep = cam.read() 
    hsv = cv2.cvtColor(kep, cv2.COLOR_BGR2HSV)

    l_h  = cv2.getTrackbarPos('L-H', 'csuszka')
    l_s  = cv2.getTrackbarPos('L-S', 'csuszka')
    l_v  = cv2.getTrackbarPos('L-V', 'csuszka')
    u_h  = cv2.getTrackbarPos('U-H', 'csuszka')
    u_s  = cv2.getTrackbarPos('U-S', 'csuszka')
    u_v  = cv2.getTrackbarPos('U-V', 'csuszka')
    lover_red = np.array([l_h , l_s, l_v])
    upper_red = np.array([u_h , u_s  , u_v])
    

    mask = cv2.inRange(hsv, lover_red, upper_red)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel)
    if int(cv2.__version__[0]) > 3:
        
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        terulet = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if terulet > 800:
            cv2.drawContours(kep, [approx], 0, (240,128,0),2)

            if len (approx) == 4:
                cv2.putText(kep, 'Bankjegy', (x,y), betutipus, 1, (240,128,0))
                bankjegy()
            if 5 < len(approx) < 200:
                cv2.putText(kep, 'Apro', (x,y), betutipus, 1, (240,128,0),1, cv2.LINE_AA)
                apro()
    cv2.imshow('Ablak',kep)
    cv2.imshow("Maszk", mask)
    
    
    bill = cv2.waitKey(1)
    if bill == 27:
        break


cam.release()
cv2.destroyAllWindows()