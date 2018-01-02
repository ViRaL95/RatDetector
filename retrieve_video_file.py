import numpy
import imutils
import cv2
import csv



class Point:
    def __init__(self, x_coordinate=None, y_coordinate=None, time=None, frame_number=None):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.time = time
        self.frame_number = frame_number



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
        time = int(video.get(cv2.CAP_PROP_POS_MSEC))
        print("time is {}".format(time))
        #if the frame was not grabbed
        if not grabbed:
            break 
        #frame = cv2.GaussianBlur(frame, (11, 11), 0)
        #frame = cv2.erode(frame, None, iterations=2)
        #frame = cv2.dilate(frame, None, iterations=2)
        mask =  cv2.inRange(frame, miceLower, miceUpper)
        params = cv2.SimpleBlobDetector_Params()
        params.filterByConvexity = True
        params.minConvexity = 0.4
        params.minThreshold = 200
        params.maxThreshold = 255
        params.filterByArea = True
        params.minArea = 300
        detector = cv2.SimpleBlobDetector_create(params)
        key_points = detector.detect(mask)
        
        image_with_keypoints = cv2.drawKeypoints(mask, key_points, numpy.array([]))
        cv2.imshow('image_with_keypoints', image_with_keypoints)        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        key_points_large.append(key_points)
    create_or_edit_csv_file(key_points_large)


 
            
def create_or_edit_csv_file(key_points):
    with open ('key_points2.csv', 'w+') as csv_file:
        file_stream_writer = csv.writer(csv_file)
        print("key_points is {}".format(key_points))
        print(type(key_points))
        for key_point in key_points:
            for x_and_y in key_point:
                file_stream_writer.writerow(["{} {}".format(x_and_y.pt[0], x_and_y.pt[1])])




         
a = Point()
a.x_coordinate = 5
a.y_coordinate = 10


if __name__ == '__main__':
    retrieve_info_from_video()    
