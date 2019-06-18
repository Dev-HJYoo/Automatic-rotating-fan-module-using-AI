######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Yoo Hyeong Jun
# Date: 6/18/19
# Description: 
# This program uses a TensorFlow-trained classifier to perform object detection.
# It loads the classifier uses it to perform object detection on a webcam feed.
# It draws boxes and scores around the objects of interest in each frame from
# the webcam.
# Using Socket Transport
# Transport Presentence ( Left - 1, Right - 2, Rotation - 3 )

## Some of the code is copied from EdjeElectronics at
## https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10

## but I changed it to make it more understandable and usable to me
## '##' is the comment i put

# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import socket

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

## A function that returns a buffer received from socket
def recvall(sock, count):
    # Byte string
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

## PC_IP
HOST='PC_IP'
PORT= 8485

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')
 
## Specify the server's IP and port number
s.bind((HOST,PORT))
print('Socket bind complete')

## Wait for the client to connect. (Up to 10 client connections)
s.listen(10)
print('Socket now listening')

## Connection, conn is socket object, addr is the address bound to the socket 
conn,addr=s.accept()

d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
d.connect(('Raspberry_IP',8486))



# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 1

# Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')




while(True):
    boxss = []
    # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value

    ## Image Length
    length = recvall(conn, 16)
    
    ## Image Data
    stringData = recvall(conn, int(length))
    
    ## String to Numpy array
    data = np.fromstring(stringData, dtype = 'uint8')

    ## Object detection Code
    
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    height, width, channel = frame.shape
    frame_expanded = np.expand_dims(frame, axis=0)
    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})


    # Draw the results of the detection (aka 'visulaize the results')
    vis_util.visualize_boxes_and_labels_on_image_array( ## I change vis_util.visualize_boxes_and_labels_on_image_array
        frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        boxss, ## boxss is x max,min y max,min array
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.90) ## Thresh Hold
    
    ## ymin,xmin,ymax,xmax
    for i,num in enumerate(boxss):
        boxss[i] = num * 480

    ## Number of objects 
    sizes = int(len(boxss)/4)

    ## Motor state
    state = 0

    ## 1 person
    if sizes == 1 :

        ## my center
        centerx = int((boxss[3]+boxss[1])/2)
        ## web cam center
        width = int(width/2)

	## left
        if width - centerx > 0: 
            print("left")
            state = 1

        ## right
        else:
            print("right")
            state = 2

    ## 2 or more persons
    else :
        print("spin")
        state = 3

    ## to raspberry pi Transport state
    d.sendall(str(state).encode('utf-8'))
    
    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('Object detector', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
video.release()
cv2.destroyAllWindows()

