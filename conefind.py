#!/usr/bin/python3

import cv2
import numpy as np

centerX = 160
centerY = 120
#hsvcopy = None
cropped = None

def on_mouse(event, x, y, flags, param):
  if event==cv2.CV_EVENT_LBUTTONDOWN:
    print("clicked ", x, ", ", y, ": ", cropped[y,x])
    #global centerX
    #global centerY
    #centerX = x
    #centerY = y

if __name__ == '__main__':
  cam = cv2.VideoCapture(0)
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
  # https://docs.opencv.org/2.4/modules/core/doc/old_basic_structures.html?highlight=createimage#IplImage*%20cvCreateImage(CvSize%20size,%20int%20depth,%20int%20channels)
  # size, depth, channels 
  #polar = cv2.CreateImage((360, 360), 8, 3)
  polar = cam.read()
  #cropped = cv2.CreateImage((360, 40), 8, 3)
  cropped = cam.read()
  #hsvcopy = cv2.CreateImage((360, 40), 8, 3)
  #img = cv2.CreateImage((320, 240), 8, 3)
  img = cam.read()
  #cones = cv2.CreateImage((360, 40), 8, 1)
  cones = cam.read()
  #arr = cv2.CreateImage((360, 40), 8, 1)
  #gee = cv2.CreateImage((360, 40), 8, 1)
  #bee = cv2.CreateImage((360, 40), 8, 1)

  #hue = cv2.CreateImage((360, 40), 8, 1)
  #sat = cv2.CreateImage((360, 40), 8, 1)
  #val = cv2.CreateImage((360, 40), 8, 1)

  cv2.namedWindow('cam')
  cv2.resizeWindow('cam', 320,240)

  cv2.namedWindow('unwrapped')
  cv2.resizeWindow('unwrapped', 360,40)
  #cv2.NamedWindow('hsvcopy')
  #cv2.ResizeWindow('hsvcopy', 360,40)

  #cv2.NamedWindow('polar')
  cv2.namedWindow('cones')
  
  #cv2.NamedWindow('hue')
  #cv2.NamedWindow('sat')
  #cv2.NamedWindow('val')
  
  #cv2.NamedWindow('arr')
  #cv2.NamedWindow('gee')
  #cv2.NamedWindow('bee')

  cv2.setMouseCallback('unwrapped', on_mouse)
  #on_mouse(cv2.CV_EVENT_LBUTTONDOWN, img.width/2, img.height/2, None, None)

  #lower = cv2.Scalar(200, 100, 50) #apparently scalars are RGB even when the image is BGR?
  #lower = cv2.Scalar(50, 100, 200) 
  #upper = cv2.Scalar(100, 200, 255)
  lower = np.array([50, 100, 200])
  upper = np.array([100, 200, 255])

  M = 69

  while True:
    result, img = cam.read()
    if not result:
      break

    # Flag was CV_INTER_NN before, but have no idea what that is.
    polar = cv2.logPolar(img, (centerX, centerY), M+1, cv2.WARP_FILL_OUTLIERS) #possible speedup - get subrect src
    #cropped = cv2.GetSubRect(polar,(280,0,40,360))
    #cv2.Transpose(cropped, cropped)
    #cv2.transpose(cv2.getSubRect(polar,(280,0,40,360)), cropped)
    cropped = cv2.transpose(polar[280:0,40:360])
    cropped = cv2.flip(cropped, 1) #just for viewing

    cones = cv2.inRange(cropped, lower, upper)
    cones = cv2.erode(cones) # just once might be too much

    k = cv2.createStructuringElementEx(3, 47, 1, 23, cv2.CV_SHAPE_RECT)
    cv2.dilate(cones, cones, k) 
    
    #cv2.Split(cropped, bee, gee, arr, None)
    #cv2.CvtColor(cropped, hsvcopy, cv2.CV_BGR2HSV)
    #cv2.Split(hsvcopy, hue, sat, val, None)

    cv2.imshow('cam', img)
    #cv2.ShowImage('polar', polar)
    cv2.imshow('cones', cones)
    #cv2.ShowImage('hsvcopy', hsvcopy)
    cv2.imshow('unwrapped', cropped)

    #cv2.ShowImage('hue', hue)
    #cv2.ShowImage('sat', sat)
    #cv2.ShowImage('val', val)

    #cv2.ShowImage('arr', arr)
    #cv2.ShowImage('gee', gee)
    #cv2.ShowImage('bee', bee)


    #print "(2,2) = ", arr[2,2], ", ", gee[2,2], ", ", bee[2,2]
    key = cv2.waitKey(30)
    #print "key ",key
    if key == 27:
        break
    elif key == 65362:
        print("M=",M+1)
        M = (M + 5)%100
    elif key == 65364:
        print("M=",M+1)
        M = (M - 5)%100
  
  cv2.release()
  cv2.destroyAllWindows()
