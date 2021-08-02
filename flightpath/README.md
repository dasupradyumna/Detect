# Drone Flight Path Estimation

A very simple script which uses SURF algorithm to pick features from every frame of the flight video. It then uses a
brute force matcher to check the similarity between consecutive SURF features. We then use the "most" similar features
and calculate the distance moved (in pixels) by each feature between 2 frames. This gives us a rough estimate of the
distance that the drone has moved. 

The distance mapped in the final image is not to scale, since it is not calibrated to the real world distance, but is
measured in image pixels.