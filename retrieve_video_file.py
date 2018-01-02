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
        time_at_current_frame = int(video.get(cv2.CAP_PROP_POS_MSEC))
        frame_number_at_current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        #if the frame was not grabbed
        if not grabbed:
            break 
        frame = cv2.GaussianBlur(frame, (11, 11), 0)
        frame = cv2.erode(frame, None, iterations=2)
        frame = cv2.dilate(frame, None, iterations=2)
        mask =  cv2.inRange(frame, miceLower, miceUpper)
        params = cv2.SimpleBlobDetector_Params()
        params.filterByConvexity = True
        params.minConvexity = 0.7
        params.minThreshold = 200
        params.maxThreshold = 255
        params.filterByArea = True
        params.minArea = 300
        detector = cv2.SimpleBlobDetector_create(params)
        key_points = detector.detect(mask)
        image_with_keypoints = cv2.drawKeypoints(mask, key_points, numpy.array([]))
        cv2.imshow('image_with_keypoints', image_with_keypoints)
        key_points.append(time_at_current_frame)
        key_points.append(frame_number_at_current_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        key_points_large.append(key_points)
    print(key_points_large)
    create_or_edit_csv_file(key_points_large)


 
            
def create_or_edit_csv_file(frames):
    with open ('key_points2.csv', 'w+') as csv_file:
        file_stream_writer = csv.writer(csv_file)
        for frame in frames:
            for key_point in frame[:-2]:
                time_at_current_frame = frame[-2]
                frame_number_at_current_frame = frame[-1]
                x_coordinate = key_point.pt[0]
                y_coordinate = key_point.pt[1]
                file_stream_writer.writerow(["{} {} {} {}".format(x_coordinate, y_coordinate, time_at_current_frame, frame_number_at_current_frame)])




         


if __name__ == '__main__':
    retrieve_info_from_video()    
