import cv2 
import mediapipe as mp
import time

import serial
import time
ser =serial.Serial(port='COM6', baudrate=115200)

class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.75, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, 
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
 
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
 
    def findPosition(self, img, handNo=0, draw=True):
 
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
 
        return lmList
    
#setting numbers for each gestures
def getNumber(ar):
    s = ""
    for i in ar:
        s += str(ar[i]);

    if(s == "00000"):
        return (0)
    elif(s == "01000"):
        return(1)
    elif(s == "01100"):
        return(2)
    elif(s == "01110"):
        return(3)
    elif(s == "01111"):
        return(4)
    elif(s == "11111"):
        return(5)
    # elif(s == "01001"):
    #     return(6)
    # elif(s == "01011"):
    #     return(7)
    
import cv2
pTime = 0
cTime = 0
cv2.namedWindow("preview")

wcam, hcam = 640, 480
vc = cv2.VideoCapture(0)
vc.set(3, wcam)
vc.set(4, hcam)

detector = handDetector()
if vc.isOpened(): # try to get the first frame
    rval, img = vc.read()
else:
    rval = False

number_old=1000
count = 0
number = 0
number_sum =0
number_list=[]
number_string_n=""
number_string="000"
ok_flash=False
success ="-"

#BANG MA CODE

sv1="SV1: DINH THI PHUONG  THAO"
ms1="MSSV:1953020014 "
sv2="SV2: NGUYEN QUYNH TRANG"
ms2="MSSV:1953020082 "
gvhd="GVHD: TS.TRAN QUOC KHAI"
s0= "CODE: THIET BI   "
s1= "10- : DEN QUAT TANG 1" 
s2= "11- : TV QUAT  TANG 1"
s3= "20- : TV TANG 2" 
s4= "21- : DEN QUAT TANG 2" 
s5= "30- : DEN QUAT TANG 3" 
s6= "31- : DEN QUAT SAN VUON"
s7= "00- : GARA CONG"

s8= "55-: tat ca thiet bi"
s9= "CODE+0: ON, CODE+5: OFF"
#CHUONG TRINH CHINH
while rval:
    cv2.imshow("preview", img)
    rval, img = vc.read()
    cv2.putText(img, sv1, (0, 140), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2) 
    cv2.putText(img, ms1, (0, 160), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
    cv2.putText(img, sv2, (0, 180), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2) 
    cv2.putText(img, ms2, (0, 200), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2) 
    cv2.putText(img, gvhd, (0,220), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)  

    cv2.putText(img, s0, (0, 280), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2) 
    cv2.putText(img, s1, (0, 300), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1) 
    cv2.putText(img, s2, (0, 320), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1) 
    cv2.putText(img, s3, (0, 340), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1) 
    cv2.putText(img, s4, (0, 360), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1) 
    cv2.putText(img, s5, (0, 380), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1) 
    cv2.putText(img, s6, (0, 400), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1) 
    cv2.putText(img, s7, (0, 420), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1) 
    cv2.putText(img, s8, (0, 440), cv2.FONT_HERSHEY_PLAIN, 1, (100, 0,100),2)
    cv2.putText(img, s9, (0, 460), cv2.FONT_HERSHEY_PLAIN, 1, (100, 0,100),2)
    cv2.rectangle(img, (10, 30), (180, 120), (0, 255, 0), cv2.FILLED)  
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
            # print(lmList[4])
        tipId = [4, 8, 12, 16, 20]
#     tipId = [1, 10, 20, 30, 40]
    if(len(lmList) != 0):
        fingers = []
        # thumb
        if(lmList[tipId[0]][1] > lmList[tipId[0]-1][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 fingers
        for id in range(1, len(tipId)):

            if(lmList[tipId[id]][2] < lmList[tipId[id]-2][2]):
                fingers.append(1)

            else:
                fingers.append(0)

        #draw landmarks,text for each gestures
        
        # cv2.putText(img, str(getNumber(fingers)), (45, 375), cv2.FONT_HERSHEY_PLAIN,
        #                              10, (255, 0, 0), 20)
         
        count = count + 1
        if getNumber(fingers)!= None:
            number_sum = number_sum + getNumber(fingers)
        if count == 10:
            number = number_sum / count
            count = 0
            number_sum = 0 
               
            
            if number - int(number) == 0:
                
                if number_old != number:
                    # print(number)
                    ser.flushInput()
                    number = int(number)
                    number_list.append(number)
                    print(number_list)
          
                number_old = number
            elif abs(number - int(number)) >0.1:
                number_old=100
        if len(number_list) == 1:
            number_string= str(number_list[0])+"--"   
            success = "-"        
        if len(number_list) == 2:
            number_string= str(number_list[0])+ str(number_list[1]) +'-' 
            ok_flash = False  
            success = "-"  
        if len(number_list) == 3:
            number_string= str(number_list[0])+ str(number_list[1])+str(number_list[2])                  
            number_string_n = number_string+'\n'
             
            if ok_flash==False:
               print("send")
               ser.write(number_string_n.encode())
               success ="-"
               ok_flash = True
               ser.flushInput()
            time.sleep(0.01)
        if len(number_list)>3:
            # number_string= "---" 
            if number_list[-1] == 5 or number_list[-1] == 0:
                ok_flash = False
                number_list = [number_list[0],number_list[1],number_list[-1]] 
            else:
                number_list = [number_list[0],number_list[1],number_list[2]] 
                # number_list = [] 
                

        if ser.in_waiting > 0:
                    # while(1):
            serialString = ser.readline()
            try:
                data_feedback = int(serialString.decode("Ascii"))
                if data_feedback==1111:
                    # ser.flushInput()
                    success = "OK"
                    # ok_flash = True
                         # Print the contents of the serial data
                elif data_feedback==1110:
                    ok_flash = False
                    success = "NO"
            
                print(data_feedback)
                 
            except:
                pass            
   
        print(number_string_n)     
        
        cv2.putText(img, number_string, (10, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)  
        # cv2.putText(img, str(int(number)), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 20) 
        cv2.putText(img, success, (500, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5) 
        # print(ok_flash)   
   
    else:
        # ser.write(b"1234\n")      
        # number_string="---" 
        number_list=[]
        number_old=1000
        cv2.putText(img, number_string, (10, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)  
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")