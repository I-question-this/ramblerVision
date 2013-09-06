#!/usr/bin/python

import cv
from datetime import datetime

centerX = 160
centerY = 120
#hsvcopy = None
cropped = None
img = None

def on_mouse(event, x, y, flags, param):
  if event==cv.CV_EVENT_LBUTTONDOWN:
    print "clicked ", x, ", ", y  #, ": ", img[y,x]
    global centerX
    global centerY
    centerX = x
    centerY = y

if __name__ == '__main__':
  capture = cv.CaptureFromCAM(0)
  cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
  cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
  polar = cv.CreateImage((360, 360), 8, 3)
  cropped = cv.CreateImage((360, 40), 8, 3)
  #hsvcopy = cv.CreateImage((360, 40), 8, 3)
  img = cv.CreateImage((320, 240), 8, 3)
  
  cones = cv.CreateImage((360, 40), 8, 1)

  arr = cv.CreateImage((360, 40), 8, 1)
  gee = cv.CreateImage((360, 40), 8, 1)
  bee = cv.CreateImage((360, 40), 8, 1)

  #hue = cv.CreateImage((360, 40), 8, 1)
  #sat = cv.CreateImage((360, 40), 8, 1)
  #val = cv.CreateImage((360, 40), 8, 1)

  ##GUI cv.NamedWindow('cam')
  ##GUI cv.ResizeWindow('cam', 320,240)

  ##GUI cv.NamedWindow('unwrapped')
  ##GUI cv.ResizeWindow('unwrapped', 360,40)
  #cv.NamedWindow('hsvcopy')
  #cv.ResizeWindow('hsvcopy', 360,40)

  #cv.NamedWindow('polar')
  ##GUI cv.NamedWindow('cones')
  
  #cv.NamedWindow('hue')
  #cv.NamedWindow('sat')
  #cv.NamedWindow('val')
  
  #cv.NamedWindow('arr')
  #cv.NamedWindow('gee')
  #cv.NamedWindow('bee')

  ##GUI cv.SetMouseCallback('cam', on_mouse)
  ##GUI on_mouse(cv.CV_EVENT_LBUTTONDOWN, centerX, centerY, None, None)

  # These (B,G,R) values determine the range of colors to detect as "cones".
  #Calibration A: room 817
  lower = cv.Scalar(45,  90, 160) 
  upper = cv.Scalar(90, 180, 255)

  M = 69

  while True:
    img = cv.QueryFrame(capture)
    cv.LogPolar(img, polar, (centerX, centerY), M+1, cv.CV_INTER_NN) #possible speedup - get subrect src
    #cropped = cv.GetSubRect(polar,(280,0,40,360))
    #cv.Transpose(cropped, cropped)
    cv.Transpose(cv.GetSubRect(polar,(280,0,40,360)), cropped)
    cv.Flip(cropped) #just for viewing (possible speedup)

    cv.InRangeS(cropped, lower, upper, cones)
    cv.Erode(cones, cones) # just once might be too much

    k = cv.CreateStructuringElementEx(3, 43, 1, 1, cv.CV_SHAPE_RECT) # create a 3x43 rectangular dilation element k
    cv.Dilate(cones, cones, k, 2) 

    #scan top row of thresholded, eroded, dilated image, find the number of contiguous segments and their location
    s = 0 # size of contiguous segment
    ss = 0 #number of contiguous segments
    bearingToLandmarks = []
    for i in xrange(360-2):
        c = cones[0, i] #current
        n = cones[0, i+1] #next
        #print int(c),
        if (c == 0 and n == 255) or \
           (c == 255 and n == 255): # this condition marks beginning or middle of contiguous segment
            s = s + 1
            #print ".",
        elif (c == 255 and n == 0): # end of contiguous segment
            ss = ss + 1
            bearingToLandmarks.append((i-s/2, s))
            #print "! ss", ss, "@", i-s/2,
            s = 0
        #handle wraparound
        if (i == 360-2-1 and s != 0): #TODO: double check this offset
            if (cones[0,0] == 255):
                #print "edge case A"
                bearingToLandmarks[0] = ((bearingToLandmarks[0][0]-s/2)%360, bearingToLandmarks[0][1]+s) #TODO: recalculate center more accurately
            else:
                #print "edge case B"
                bearingToLandmarks.append((c-s/2, s))
    #print ".", ss, "."
    print str(datetime.now().time()), bearingToLandmarks, len(bearingToLandmarks)
    
    cv.Split(cropped, bee, gee, arr, None)
    #cv.CvtColor(cropped, hsvcopy, cv.CV_BGR2HSV)
    #cv.Split(hsvcopy, hue, sat, val, None)

    ##GUI cv.ShowImage('cam', img)
    #cv.ShowImage('polar', polar)
    ##GUI cv.ShowImage('cones', cones)
    #cv.ShowImage('hsvcopy', hsvcopy)
    ##GUI cv.ShowImage('unwrapped', cropped)

    #cv.ShowImage('hue', hue)
    #cv.ShowImage('sat', sat)
    #cv.ShowImage('val', val)

    #cv.ShowImage('arr', arr)
    #cv.ShowImage('gee', gee)
    #cv.ShowImage('bee', bee)


    #print "(2,2) = ", arr[2,2], ", ", gee[2,2], ", ", bee[2,2]
    key = cv.WaitKey(10)
    #print "key ",key
    if key == 27:
        break
    elif key == 65362:
        print "M=",M+1
	M = (M + 5)%100
    elif key == 65364:
        print "M=",M+1
	M = (M - 5)%100
  ##GUI cv.DestroyAllWindows()
