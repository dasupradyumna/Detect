import cv2
import imutils
import sys
import glob
import csv

if len(sys.argv) != 3 :                                 # exit if correct syntax is not followed
	print('Please use SYNTAX : \npython3 <file>.py <path to image directory> <control point label>\n')
	sys.exit(1)

refPoint = []
clicked = False

def tap_locate(event,x,y,flags,param) :                 # callback function for mouse clicks
	global refPoint,clicked
	if event == cv2.EVENT_LBUTTONDOWN :
		refPoint = [2*x,2*y]                            # scaling up clicked coordinates due to half size image
		clicked = True

def run_main(path) :
	global refPoint,clicked
	imageNames = glob.glob('{}/C_*.jpg'.format(path))   # list of all control point images, i.e names start with C
	imageNames = sorted(imageNames,key = lambda x : int(x.strip('.jpg').split('_')[-1]))    # sort images

	with open('{}/input{}.csv'.format(path,sys.argv[2]),'w',newline = '') as csvFile :
		csvWriter = csv.writer(csvFile,delimiter = ',',quoting = csv.QUOTE_MINIMAL)         # csv writer object

		for name in imageNames :
			img = cv2.imread(name)

			cv2.namedWindow('Touch me!')                        # create a named window
			cv2.setMouseCallback('Touch me!',tap_locate)        # link callback function to above window

			while True :
				cv2.imshow('Touch me!',imutils.resize(img,height = 540))    # display image in above window at half size
				key = cv2.waitKey(1) & 0xFF                                 # wait for key stroke (if any)
				if key == ord('q') :                                        # next image if Q is pressed
					break

			# add clicked point to csv file. if no point, then add (0,0) by default
			csvWriter.writerow([name.strip('.jpg').split('_')[-1]] + (refPoint if clicked else [0,0]))
			clicked = False

	cv2.destroyAllWindows()

if __name__ == '__main__' :
	run_main(sys.argv[1])
