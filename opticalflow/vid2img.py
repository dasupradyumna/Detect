import cv2
import imutils
import sys 

if len(sys.argv) != 2 :                 # exit if correct syntax is not followed
	print('Please use SYNTAX : \npython3 <file>.py <path to video file>\n')
	sys.exit(1)

def run_main(vid_name) :
	cap = cv2.VideoCapture(vid_name)    # create a OpenCV video capture object
	if not cap.isOpened() :             # throw error if object could not load video properly
		print('Video file not loaded correctly.')
		sys.exit(1)

	count = 0
	while True:
		ret, frame = cap.read()         # read next frame in the video
		if not ret :                    # exit if no more frames can be read
			break

		count += 1
		if count%5 != 0 :               # picking every 5th frame only
			continue

		# resize image to 1080p and save image
		frame = imutils.resize(frame,height = 1080)
		cv2.imwrite('images/F_{}.jpg'.format(int(count/5)),frame)

if __name__ == '__main__' :
	run_main(sys.argv[1])
