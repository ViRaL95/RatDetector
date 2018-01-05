import numpy
import cv2
import csv

def retrieve_info_from_video():
    """This function essentially thresholds a video, and retrieves each frame, uses blob detection to
    detect mice within each frame. An array is populated with information regarding the frame number,    the time the frame occurs in milliseconds, and the x and y coordinate of each blob. Multiple blo     bs may be detected during each frame. The masking, and the thresholds we are currently using are     being tested.
    """
    miceLower = numpy.array([150, 160, 170])
    miceUpper = numpy.array([170, 180, 190])

    #GRAB INPUTS FROM VIDEO AND MAKE POINTS
    video = cv2.VideoCapture("MVI_0781.MP4")
    key_points_large = []

    while True:
        (grabbed, frame) = video.read()

        #TIME AND FRAME NUMBER
        time_at_current_frame = int(video.get(cv2.CAP_PROP_POS_MSEC))
        frame_number_at_current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))

        #CHECK IF FRAME HAS NOT BEEN GRABBED
        if not grabbed:
            break
        frame = cv2.GaussianBlur(frame, (11, 11), 0)
        frame = cv2.erode(frame, None, iterations=2)
        frame = cv2.dilate(frame, None, iterations=2)
        mask =  cv2.inRange(frame, miceLower, miceUpper)
        params = cv2.SimpleBlobDetector_Params()

        #THRESHOLDS
        params.filterByConvexity = True
        params.minConvexity = 0.7
        params.minThreshold = 200
        params.maxThreshold = 255
        params.filterByArea = True
        params.minArea = 300

        detector = cv2.SimpleBlobDetector_create(params)

        #X AND Y COORDINATES STORED IN ARRAY
        key_points = detector.detect(mask)

        #DRAWS KEY POINTS ON EACH INDIVIDUAL FRAME
        image_with_keypoints = cv2.drawKeypoints(mask, key_points, numpy.array([]))
        cv2.imshow('image_with_keypoints', image_with_keypoints)

        #CREATES ARRAY WITH TIME AT CURRENT FRAME, FRAME NUMBER
        ey_points.append(time_at_current_frame)
        key_points.append(frame_number_at_current_frame)

        #IF USERS HITS 'Q' ON KEYBOARD VIDEO STOPS
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        key_points_large.append(key_points)
    create_or_edit_csv_file(key_points_large)

def create_or_edit_csv_file(frames):
    """ This method creates a CSV file, if it doesnt exist, and writes to it, if it does exist it 
    overwrites all information in it. The information in each row of the CSV file follows as: x coordinate, y coordinate, time at current frame, and frame number. There may exist multiple blobs for a given frame.
    """
    with open ('key_points.csv', 'w+') as csv_file:
        file_stream_writer = csv.writer(csv_file)
        for frame in frames:
            for key_point in frame[:-2]:
                time_at_current_frame = frame[-2]
                frame_number_at_current_frame = frame[-1]
                x_coordinate = key_point.pt[0]
                y_coordinate = key_point.pt[1]
                file_stream_writer.writerow(["{} {} {} {}".format(x_coordinate, y_coordinate, 
                                            time_at_current_frame, frame_number_at_current_frame)])

if __name__ == '__main__':
    retrieve_info_from_video()    
