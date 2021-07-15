import cv2
import pandas as pd
import argparse


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']


testImage = cv2.imread(img_path)
testImage = cv2.resize(testImage, (1000, 660))


clicked = False
r = g = b = xpos = ypos = 0


index=["color","color_name","hex","R","G","B"]
color_data = pd.read_csv('colors.csv', names=index, header=None)


def getColorName(R,G,B):
    minDist = 10000
    for i in range(len(color_data)):
        colorDist = abs(R- int(color_data.loc[i,"R"])) + abs(G- int(color_data.loc[i,"G"]))+ abs(B- int(color_data.loc[i,"B"]))
        if(colorDist<=minDist):
            minDist = colorDist
            cname = color_data.loc[i,"color_name"]
    return cname


def setPositionValues(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = testImage[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('Color Detector')
cv2.setMouseCallback('Color Detector',setPositionValues)

while(1):

    cv2.imshow("Color Detector",testImage)
    if (clicked):
   
        
        cv2.rectangle(testImage,(20,20), (750,60), (b,g,r), -1)

        
        displayText = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        
        cv2.putText(testImage, displayText,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        
        if(r+g+b>=600):
            cv2.putText(testImage, displayText,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
