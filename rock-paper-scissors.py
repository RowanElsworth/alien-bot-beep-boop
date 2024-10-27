#================================ ZIBZIDI DNA ================================

import mediapipe
from mediapipe import solutions
import cv2
from collections import Counter
import random
from time import sleep
import time 
import socket
import asyncio

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

user_score = 0
comp_score = 0

button = True

HOST = "192.168.212.251"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")

ret, frame = cap.read()
frame1 = cv2.resize(frame, (640, 480))
hands = handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1)
 
def findNameOfLandmark(frame1):
    list = []
    results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            for point in handsModule.HandLandmark:
                list.append(str(point).replace("<","").replace("HandLandmark.","").replace("_","").replace("[]",""))
    return list

counter = 0

def cameraLoop():
     # infinite loop that produces live feed on screen searching for hands
        while True:
            asyncio.run(listenLoop())
            ret, frame = cap.read()
            frame1 = cv2.resize(frame, (640, 480))

            list = []
            # converts video to desired colours
            results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))


            # if hand is on screen
            if results.multi_hand_landmarks != None:
                # deals with mutliple hands
                for handLandmarks in results.multi_hand_landmarks:
                    list = []
                    drawingModule.draw_landmarks(image = frame1, landmark_list = handLandmarks, connections = handsModule.HAND_CONNECTIONS)
                    for id, pt in enumerate (handLandmarks.landmark):
                        x = int(pt.x * w)
                        y = int(pt.y * h)
                        list.append([id,x,y])

            # displays camera feed
            cv2.imshow('ROCK PAPER SCISSORS', frame1)
        
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

async def buttonPress():
            
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
            c = Counter(fingers)
            up = c['up']
            down = c['down']
            
            data = await s.recv(1024)
            print(f"Received {data!r}")
            

            comp = random.choice(['rock','paper','scissors'])

            if (fingers[0] == 'up' and fingers[1] == 'up' and fingers[2] == 'down' and fingers[3] == 'down'):
                print("\nSCISSORS\n")

                if (comp == "scissors"):
                    print("COMPUTER PLAYED SCISSORS\nDRAW")
                
                elif (comp == "rock"):
                
                    print("COMPUTER PLAYED ROCK\nYOU LOSE")
                    comp_score += 1
                
                else:
                    print("COMPUTER PLAYED PAPER\nYOU WIN")
                    user_score += 1
                
            
            elif (fingers[0] == 'up' and fingers[1] == 'up' and fingers[2] == 'up' and fingers[3] == 'up'):
                print("\nPAPER\n")

                if (comp == "scissors"):
                    print("COMPUTER PLAYED SCISSORS\YOU LOSE")
                    comp_score += 1
                
                elif (comp == "rock"):
                    print("COMPUTER PLAYED ROCK\nYOU WIN")
                    user_score += 1
                
                else:
                    print("COMPUTER PLAYED PAPER\nDRAW")
                
            elif (fingers[0] == 'down' and fingers[1] == 'down' and fingers[2] == 'down' and fingers[3] == 'down'):

                print("\nROCK")
                if (comp == "scissors"):
                    print("COMPUTER PLAYED SCISSORS\nYOU WIN")
                    user_score += 1
                
                elif (comp == "rock"):
                    print("COMPUTER PLAYED ROCK\nDRAW")
                
                else:
                    print("COMPUTER PLAYED PAPER\nYOU LOSE")
                    comp_score += 1
                
            scores = "YOU vs COMP\n",user_score,comp_score
            s.sendall(scores)
            #sleep(3)

            
async def listenLoop():
    while True:
        data = s.recv(1024)
        print("data: ",data)
        if data == "Button pressed":
            buttonPress()

cameraLoop()


s.close()
cap.release()
cv2.destroyAllWindows()
