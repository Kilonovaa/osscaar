import cv2
import os

cam = cv2.VideoCapture('orionnebula.mp4')
totalFrames = cam.get(cv2.CAP_PROP_FRAME_COUNT)
c=1
currentframe=30
while c!=0:
    cam.set(cv2.CAP_PROP_POS_FRAMES, currentframe)
    ret, image = cam.read()
    if(ret):
        name='./image_data/frame'+str(currentframe)+'.jpg'
        print('Image'+name)
        cv2.imwrite(name, image)
        currentframe+=1
    c=c-1
cam.release()
cv2.destroyAllWindows()