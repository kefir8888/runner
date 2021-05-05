import cv2
import numpy as np
import time

cam = cv2.VideoCapture(2)

frame_width  = int(cam.get(3))
frame_height = int(cam.get(4))
	
out = cv2.VideoWriter("output" + str(time.time()) + ".avi", cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))


while(True):
    ret, frame = cam.read()

    if (ret == True):
    	cv2.imshow("frame", frame)
    	out.write(frame)
    	
    	key = cv2.waitKey(1) & 0xFF
    	
    	if (key == ord('q')):
    	    break
    
    else:
    	print("cannot read frame, exiting")
    	break

cam.release()
out.release()

cv2.destroyAllWindows()
