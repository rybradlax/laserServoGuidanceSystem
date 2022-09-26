#!/usr/bin python3.5
import numpy as np
import os
import sys
#from operator import itemgetter

# probs needs to be ran from models/research/object_detection/

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
sys.path.append("C:\\Users\\brady\\Desktop\\models\\research\\object_detection")
sys.path.append("C:\\Users\\brady\\Desktop\\models\\research\\object_detection\\utils")
sys.path.append("C:\\Users\\brady\\Desktop\\models\\research\\object_detection")
##
##sys.path.append("/home/nvidia")
#sys.path.append("")

#sys.path.append("/home/nvidia/Desktop/models/research/object_detection/

import tensorflow as tf
import time
import copy

from tensorflow.core.framework import graph_pb2
from utils import label_map_util
from utils import visualization_utils as vis_util
from matplotlib import pyplot as plt
from PIL import Image
import cv2
import serial
import struct

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
center = False
right = False
left = False
turn = ""


#ser = serial.Serial('COM4', 115200, timeout = 0.2)
# What model to download.
MODEL_NAME = 'newBalls'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'object-detection.pbtxt')
# Connecting the graph with tensorflow as well as the pbtxt file 
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.compat.v1.GraphDef()
  with tf.compat.v2.io.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
# Function to load image onto numpy

NUM_CLASSES = 1
label_map = label_map_util.load_labelmap('E:\\models\\research\\object_detection\\data\\object-detection.pbtxt')
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


##def load_image_into_numpy_array(image):
##  (im_width, im_height) = image.size
##  return np.array(image.getdata()).reshape(
##      (im_height, im_width, 3)).astype(np.uint8)

with detection_graph.as_default():
  with tf.compat.v1.Session(graph=detection_graph,config=tf.compat.v1.ConfigProto(allow_soft_placement=True)) as sess:
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    image_tensor = tf.compat.v1.get_default_graph().get_tensor_by_name('image_tensor:0')
    
    # consider removing some tensors for speed b/c they're not needed
    i = 0
    
    tcount, start, finish, dcaptot, dstarttot, dnettot, ale, ball, balls = 0, 0, 0, 0, 0, 0, 0, [] ,[]
    while True:
          start = time.time()
          tcapStart=time.time()
          ret,image_np = cap.read()
          tcapFin = time.time()
          image_np_expanded = np.expand_dims(image_np, axis=0)
        
          tnetStart = time.time()
          (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
          #print 'Iteration %d: %.3f sec' %(i, time.time()-start_time)
          #
          #if scores[0][0] != None:
          #print(type(scores))
          scored = scores[0].tolist()

          tnetFin = time.time()

          #################################################
          ######          score = scores[0].tolist()
          box = boxes[0].tolist()
          cnt = 0
          b = [] #ymin, ymax, xmin, xmax
          b1 = []
          for b1 in box:
        
            b1.extend([scored[cnt]])
       
            cnt += 1
          cnt = 0

##          time.sleep(1)

          b = sorted(box,key = lambda x: x[4], reverse = True)
          #b5 = max(b,key=itemgetter(2))
          #print(b[0:2])
          #print('New')
          
          
           #b5 = max(b[0:5],key=itemgetter(2))
          
          b6old = [0,0,0,0,0]
          for b6 in b[0:5]:
            if b6[2] > b6old[2] and b6[4] >.5:
              b6old = b6
              b5 = b6
              
            
       
              




          vis_util.visualize_boxes_and_labels_on_image_array(
              image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)

          boxs = np.squeeze(boxes)
          scrs = np.squeeze(scores)
          print(boxes)
          print(scrs)
          bbb = boxs[0]
          ymin, xmin, ymax, xmax = bbb
          yCenter = (ymin+ymax)/2
          xCenter = (xmin+xmax)/2
          xCenter = xCenter * 640
          yCenter = yCenter * 640
          if xCenter >= 630 and xCenter < 650:
                center = True
                left = False
                right = False
                turn = "Center"
          elif xCenter < 630:
                right = False
                left = True
                center = False
                turn = "Left"
          elif xCenter >= 650:
                right = True
                left = False
                right = False
                turn = "Right"
          if(scrs[0] > .8):
                if turn == 'Right':
                      if 1280 - xCenter < 300:
                          #transmitData.send2('c') # 10 degrees
                          s = 'c'
                          ser.write(s.encode())
                        # print("+10 degrees")
                      elif 1280-xCenter<450 and 1280-xCenter>=300:
                          #transmitData.send2('x') # 5 degrees
                          s = 'x'
                          ser.write(s.encode())
                         # print("+5 degrees")
                      elif 1280-xCoordList[idx]<550 and 1280-xCenter>=450:
                          #transmitData.send2('z') # 3 degrees
                          s = 'z'
                          ser.write(s.encode())
                         # print("+3 degrees")
                      elif 1280-xCenter<630 and 1280-xCenter>=550:
                          #transmitData.send2('l') # 1 degree
                          s = 'l'
                          ser.write(s.encode())
                        #  print("+1 degree")
                elif turn == 'Left':
                      if 1280-xCenter > 980:
                          #transmitData.send2('m') # 10 degrees
                          s = 'm'
                          ser.write(s.encode())
                         # print("-10 degrees")
                      elif 1280-xCenter>830 and 1280-xCenter<=980:
                          #transmitData.send2('n') # 5 degrees
                          s = 'n'
                          ser.write(s.encode())
                         # print("-5 degrees")
                      elif 1280-xCenter>730 and 1280-xCenter<=830:
                          #transmitData.send2('b') # 3 degrees
                          s = 'b'
                          ser.write(s.encode())
                         # print("-3 degrees")
                      elif xCenter - 1280>650 and 1280-xCenter <=730:
                          #transmitData.send2('v') # 1 degree
                          s = 'v'
                          ser.write(s.encode())





            ####################################################
          if True:
                        screenText = 'Moving '+turn
                        cv2.line(image_np,(610,360),(670,360),(255,0,0),2) #draw line in middle of screen
                        cv2.line(image_np,(640,330),(640,390),(255,0,0),2) #draw line in middle of screen
                        font                   = cv2.FONT_HERSHEY_SIMPLEX
                        bottomLeftCornerOfText = (850,360)
                        fontScale              = 1
                        fontColor              = (255,255,255)
                        lineType               = 2
                        cv2.putText(image_np, screenText, 
                        bottomLeftCornerOfText, 
                        font, 
                        fontScale,
                        fontColor,
                        lineType)

          cv2.imshow('object_detection',image_np) #, cv2.resize(image_np, (800,600))
          #'''
          '''finish = time.time()
          dcap = tcapFin - tcapStart
          dcaptot = dcaptot + dcap
          dstart = finish - start
          dstarttot = dstarttot + dstart
          dnet = tnetFin - tnetStart
          dnettot = dnettot + dnet
          tcount +=1
          if tcount == 100:
              tcount = 0
              print ('totalTime: ', dstarttot/100 , '  Capture: ' , dcaptot/100 , '  NeuralNet: ', dnettot/100)
              dcaptot, dstarttot, dnettot = 0, 0, 0'''
          if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.distroyAllWindows()
            break

          
