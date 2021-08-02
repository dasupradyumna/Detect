import cv2
import glob
import csv
import sys
import imutils
import numpy as np

if len(sys.argv) != 2 :  # exit if correct syntax is not followed
	print('Please use SYNTAX :\npython3 <file>.py <path to images directory>')
	sys.exit(1)

# dictionary of parameters for Optical Flow algorithm
LKOF_param = dict( winSize = (15,15),
					maxLevel = 5,
					criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

refList = []
def readCSV(C_images,N_corners,path) :
	global refList
	data = np.zeros((C_images,N_corners,2))                 # (x,y) coordinates of all corners in all reference images

	for i in range(N_corners) :
		with open('{}/input{}.csv'.format(path,i+1),'r') as csvFile :   # open corresponding csv image of each corner
			im = 0
			Reader = csv.reader(csvFile,delimiter = ',',quoting = csv.QUOTE_MINIMAL)  # csv reader object
			for ref,x,y in Reader :                         # iterate over each row in the csv file
				if ref not in refList :
					refList.append(ref)
				data[im][i][0] = x
				data[im][i][1] = y
				im += 1

	print('Finished reading data from csv files.\n')
	return data

def writeCSV(data,path) :
	global refList
	C_images, N_corners = data.shape[:-1]

	with open('{}/output.csv'.format(path), 'w', newline = '') as csvFile :
		Writer = csv.writer(csvFile, delimiter = ',', quoting = csv.QUOTE_MINIMAL)  # csv writer object
		for im in range(C_images) :                 # iterate through images
			for i in range(N_corners) :             # iterate through corners
				if np.all(data[im][i] != 0) :       # if (0,0), skip
					if im+1 in refList :
						Writer.writerow(['C_{}.jpg'.format(im+1)]+[i+1]+list(data[im][i]))
					else :
						Writer.writerow(['F_{}.jpg'.format(im+1)]+[i+1]+list(data[im][i]))

	print('Finished writing data to csv files.\n')

def run_optical_flow(path) :
	imageNames = glob.glob('{}/*.jpg'.format(path))   # list of all images in the directory
	imageNames = sorted(imageNames,key = lambda x : int(x.strip('.jpg').split('_')[-1]))   # sort above list of images
	
	nRef = 14       # int(input('No. of reference images C = '))
	nCorners = 8    # int(input('No. of reference corners N = '))
	corners_data = readCSV(nRef, nCorners, path)  # numpy array of coordinates of all corners in the reference images
	out = cv2.VideoWriter('trackbox.mp4',cv2.VideoWriter_fourcc(*'mp4v'),30.0,(960,540))

	gray_old = nonzero = old_nz = None
	new = None                                                  # stores updated coordinates after flow calculation
	count = 0                                                   # index for reference images
	out_data = []                                               # list that will be stored into csv after loop
	total = len(imageNames)
	finished = 0                                                # book keeping number
	for name in imageNames :
		img = cv2.imread(name)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)            # next iteration grayscale converted image

		if name.strip('.jpg').split('_')[-2][-1] == 'C' :       # if current image is reference image (C_*.jpg)
			old = corners_data[count]                           # corner coordinates from next reference image
			nonzero = np.where(old != [0,0])                    # indices of nonzero coordinates
			old_nz = old[nonzero]                               # removing (0,0) pairs
			old_nz = old_nz.reshape(-1,2).astype(np.float32)
			for a,b in old_nz :                                 # draw the points in red on the image
				img = cv2.circle(img, (int(a),int(b)), 5, (0,0,255), -1)

			gray_old = gray                                     # skip optical flow step and set current image to old
			new = np.zeros_like(old)
			out_data.append(old)
			count += 1
		else :
			# calculate optical flow of the control points
			new_nz, ret, error = cv2.calcOpticalFlowPyrLK(gray_old, gray, old_nz, None, **LKOF_param)
			new[nonzero] = new_nz.ravel()                       # update the old coordinates
			ret = ret.ravel()
			good_new = new_nz[np.nonzero(ret)]                  # check if optical flow output is valid
			for a,b in good_new :                               # draw the points in red on the image
				img = cv2.circle(img, (int(a),int(b)), 5, (0,0,255), -1)

			# swapping data for next iteration
			gray_old = gray
			old_nz = new_nz
			out_data.append(new)

		# display the image with the tracked points in red color, press Q to stop algorithm
		cv2.imshow('Optical Flow', imutils.resize(img, width = 960))
		out.write(imutils.resize(img, width = 960))  # write frame to video
		if cv2.waitKey(1) & 0xFF == ord('q') :
			break

		finished += 1
		print('Optical Flow : ',finished, '/',total)            # book keeping during execution

	out_data = np.array(out_data)
	cv2.destroyAllWindows()
	out.release()
	print('Optical Flow : Tracking completed \n')

	writeCSV(out_data,path)                                     # write the tracked coordinates to csv files

if __name__ == '__main__' :
	run_optical_flow(sys.argv[1])
