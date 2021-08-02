# run on python3.5
# the flight path extracted is not to scale and execution takes a couple of minutes

import numpy as np
import cv2
from matplotlib import pyplot as plt
import imutils

surf = cv2.xfeatures2d.SURF_create()	# initializing surf algorithm
surf.setHessianThreshold(4000)
surf.setUpright(True)

bf = cv2.BFMatcher()		# initializing bruteforce matcher

cap = cv2.VideoCapture("Estimate flight path.mp4")
_,frame1 = cap.read()
frame1 = imutils.resize(frame1,width = 1280)
kp1,des1 = surf.detectAndCompute(frame1,None) # query image (first frame)

pathx = [0]		# list of the path points
pathy = [0]
ret,frame2 = cap.read()
while(frame2 is not None):	

	frame2 = imutils.resize(frame2,width = 1280)
	kp2, des2 = surf.detectAndCompute(frame2,None) # train image to compare with query
	
	matches = bf.knnMatch(des1,des2,k=1)
	match_sorted = sorted(matches,key=lambda x:x[0].distance)	# finds the best matches and sorts the list
	Sx = 0
	Sy = 0
	S = 0
	if(len(match_sorted)<5):		# skips any frames with less than 5 features to work with
		frame1 = frame2.copy()
		kp1 = kp2.copy()
		des1 = des2.copy()
		ret, frame2 = cap.read()
		continue
	for i in range(5):						# finds the best out of the 5 features to measure the displacement
		ind1 = match_sorted[i][0].queryIdx
		ind2 = match_sorted[i][0].trainIdx
		pt1 = (int(kp1[ind1].pt[0]),int(kp1[ind1].pt[1]))
		pt2 = (int(kp2[ind2].pt[0]),int(kp2[ind2].pt[1]))
		xdisp = pt1[0]-pt2[0]
		ydisp = pt2[1]-pt1[1]
		if(S < xdisp**2+ydisp**2):
			S = xdisp**2+ydisp**2
			Sx = xdisp
			Sy = ydisp
		cv2.line(frame1, pt1, pt2, (255,0,0), 5-i)
	
	pathx.append(pathx[-1]+Sx)		# appending the list of path points
	pathy.append(pathy[-1]+Sy)
	
	frame1 = frame2.copy()
	kp1 = kp2.copy()
	des1 = des2.copy()
	ret, frame2 = cap.read()


plt.plot(pathx, pathy, 'r')		# plotting the path
plt.title('Extracted Flight Path',va = 'bottom')
plt.xlabel('Horizontal displacement')
plt.ylabel('Height')
plt.show()