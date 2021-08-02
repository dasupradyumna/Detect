# Optical Flow Tracking of Target Object

Given a video of any object to be tracked, we extract the video into a sequence of images and then **manually** choose
a number of images as key frames, in which we will mark the control points that will be used the sparse optical flow 
algorithm to generate a sequence of tracked coordinates. We need to choose these key frames to be those where an 
existing control point goes out of view or a new potential control point comes into view, due to the movement of the 
camera (i.e, the pose of the object changes significantly). Hence, this is not a fully automated process, it still
requires human intervention to function properly. But, if the key frames are chosen well, the script produces an output
that is seamless, with no hint of manual keyframes being used.

Here, it is a 3-stage process of running the python files consecutively :
1) We run `vid2img.py` with target video as the command line argument. This script extracts every 5th frame from the 
   video, resizes it to 1080p and saves all the extracted images to a directory named "images" in CWD.
2) Next, select key frames out of all the extracted images. Decide on a set of control points through the duration of
   the video. Run `setCpts.py` with 2 command line arguments - [ path to image directory ] and [ index of the control
   point being selected ]. This script generates `input{}.csv` files in "images" directory which contains the
   coordinates of the control points in the respective key frames, where `{}` contains the index of the control point.
3) Once the above script is run for all the chosen control points, run `trackOF.py` with "images" directory as command
   line argument. This script will perform the optical flow algorithm, using the `.csv` files generated in the previous
   step. It outputs a video with the tracked points drawn in red and an `output.csv` file which contains the tracked
   coordinate values for every image in the directory.

Link to output video : https://drive.google.com/file/d/1Tt59iTwbr7_l9AHN-wLntoqs61d9WlzN/view?usp=sharing