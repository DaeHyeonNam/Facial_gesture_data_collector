from typing import Tuple
import cv2
import socket
import threading 
import random
import os.path
import time
import os


'''
For collecting video data
'''
if not os.path.exists("./1"):
    for i in range(1,6):
        os.makedirs("./"+str(i)+"/")

def current_milli_time():
    return round(time.time() * 1000)

prevTime = current_milli_time()



'''
Setting for general purpose
'''
dataIndex = 0


'''
0: Others
1: Left Wink
2: Right Wink
3: Both Wink
4: Upper eyebrow
5: Lower eyebrow
'''
curIndex = 0


'''
Setting for udp
'''
ReceivingPort = 3012
SendingPort = 3008
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', ReceivingPort))

def sendUDP(data):
    print(address)
    sock.sendto(str.encode(data), address)

def receivingUDP():
    loopCount = 0
    global isRecording
    global isSent
    global isTestMode
    global address
    isRecording = False
    isSent = False

    while(True):
        data, addr = sock.recvfrom(128)
        dataStr = data.decode('ascii')

        
        if(dataStr[:4] == "test"):
            addrList = list(addr)
            addrList[1] = int(dataStr[4:])
            address = tuple(addrList)
            print("ack")
            
            isTestMode = True
            print("Test mode is activated")
            
            
        elif(dataStr[:4] == "real"):
            addrList = list(addr)
            addrList[1] = int(dataStr[4:])
            address = tuple(addrList)
            print("ack")
            
            isTestMode = False
            print("Real mode is activated")
        loopCount += 1


t = threading.Thread(target = receivingUDP)
t.daemon = True
t.start()



'''
Setting for video capture
'''
capture = cv2.VideoCapture(0)
 
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')


'''
Main loop
'''
while (True):
    ret, frame = capture.read()
     
    if ret:
        cv2.imshow('video', frame)
        #videoWriter.write(frame)
    input = cv2.waitKey(1)
    if input == 27:
        break
    elif input == 99:
        #c
        # save previous video
        
        # send next index
        if(not isSent):
            global videoWriter
            global filePath 
            
            isSent = True
            curIndex = random.randint(1,5)
            
            fileList = os.listdir('./'+str(curIndex))
            filePath = './'+str(curIndex)+'/'+str(len(fileList))+'.avi'
            
            if(not isTestMode):
                videoWriter = cv2.VideoWriter(filePath, fourcc, 30.0, (640,480))
            sendUDP(str(curIndex))
            prevTime = current_milli_time()
            isRecording = True
        else:
            print("wait")

    elif input == 122:
        #z
        if(not isTestMode):
            os.remove(filePath)
        sendUDP('delete')
        
    if(isRecording and not isTestMode):
        videoWriter.write(frame)
    if(isRecording and prevTime+2000 < current_milli_time()):
        isRecording = False;
        isSent = False;
        if(not isTestMode):
            videoWriter.release()
        
 
capture.release()
videoWriter.release()
 
cv2.destroyAllWindows()
