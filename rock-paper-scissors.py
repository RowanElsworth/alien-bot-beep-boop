#================================ ZIBZIDI DNA ================================

import mediapipe
import cv2
from collections import Counter
import random
from time import sleep
import time 

#draws hand framework over the hand in real time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

cap = cv2.VideoCapture(0)
results = ['rock','paper','scissors']
#video dimensions
h = 480
w = 640
#sets fingertips/middle of hand
tip = [8,12,16,20]
mid = [6,10,14,18]
fingers = []
finger = []

def findNameOfLandmark(frame1):
    list = []
    results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            for point in handsModule.HandLandmark:
                list.append(str(point).replace("<","").replace("HandLandmark.","").replace("_","").replace("[]",""))
    return list

counter = 0

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
    
    # infinite loop that produces live feed on screen searching for hands
    while True:
        ret, frame = cap.read()
        frame1 = cv2.resize(frame, (640, 480))

        list = []
        # converts video to desired colours
        results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

        # displays camera feed
        cv2.imshow('ROCK PAPER SCISSORS', frame1)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        # if hand is on screen
        if results.multi_hand_landmarks != None:
            # deals with mutliple hands
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
                list = []
                for id, pt in enumerate (handLandmarks.landmark):
                    x = int(pt.x * w)
                    y = int(pt.y * h)
                    list.append([id,x,y])

        print("list = ", list)
        a = list
        b = findNameOfLandmark(frame1)

        if len(b and a) != 0:
            fingers = []
            for id in range(0,4):
                # checks for each finger in turn using hand landmark numbers
                if tip[id] == (id*4)+8 and mid[id] == (id*4)+6:
                    # checks if fingertip is higher than middle joint
                    # "is finger up"
                    if (a[tip[id]][2:] < a[mid[id]][2:]):
                        fingers.append('up')
                    else:
                        fingers.append('down')


            print("fingers: ", fingers)
            print("b: ", b)
            c = Counter(fingers)
            up = c['up']
            down = c['down']
                
            
cap.release()
cv2.destroyAllWindows()
