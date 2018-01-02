import numpy
import imutils
import cv2
import csv

#THRESHOLD
#if the mice is between these two thresholds it will mask it to white
def retrieve_info_from_video():
    """This function essentially retrieves information from a mp4 file and finds the center
    points of each rat.


    """
    miceLower = numpy.array([150, 160, 170])
    miceUpper = numpy.array([170, 180, 190])

    #GRAB INPUTS FROM VIDEO AND MAKE POINTS
    video = cv2.VideoCapture("MVI_0781.MP4")
    key_points_large = [] 

    while True:
        #grabbed if the next frame was recieved or not. Frame will contain the next frame
        (grabbed, frame) = video.read()
        #if the frame was not grabbed
        if not grabbed:
            break
         
        #cv2.GaussianBlur(frame, (11, 11), 0)
        mask = cv2.inRange(frame, miceLower, miceUpper)
        #cv2.erode(mask, None, iterations=2)
        #cv2.dilate(mask, None, iterations=2)

        params = cv2.SimpleBlobDetector_Params()
        params.filterByConvexity = True
        params.minConvexity = 0.4
        params.minThreshold = 200
        params.maxThreshold = 255
        params.filterByArea = True
        params.minArea = 300
        detector = cv2.SimpleBlobDetector_create(params)
        key_points = detector.detect(255-mask)
        image_with_keypoints = cv2.drawKeypoints(mask, key_points, numpy.array([]))
        key_points_large.append(key_points)
    create_or_edit_csv_file(key_points)


 
            
def create_or_edit_csv_file(key_points):
    with open ('key_points.csv', 'r+') as csv_file:
        file_stream_writer = csv.writer(csv_file)
        abc = csv.writer(csv_file)
        for key_point in key_points:
            abc.writeRow(key_point)






if __name__ == '__main__':
    retrieve_info_from_video()
