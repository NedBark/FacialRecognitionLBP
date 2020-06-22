import cv2
import os
import numpy as np
import datetime
import sendEmail
from guizero import App, Text, PushButton, TextBox, warn, info, Box, Window

def sendMail():
        sendEmail.main()
        sendMail.__code__= (lambda:None).__code__

def check_cod():
        #print("WE HERE")
        f = open("UserLogin.txt", "r")
        usrs = {}
        codes = []
        for line in f:
                line = line.strip()
                split = line.split(".")
                print(split)
                usrs[int(split[0])]=split[1]
                codes.append(int(split[2]))
        f.close()

        cod=txtBox_code.get()
        print(cod)
        print(codes)
        cod = int(cod)
        if(cod in codes):
                txt.show()
                txt2.hide()
                exit()
        else:
                txt2.show()
                txt.hide()

app1 = App(title="Welcome Home", visible=False)
app2 = App(title="Check the code", visible=False)
box = Box(app2, align="top", width="fill")
txt = Text(box, align="right", text = "Welcome home", visible=False)
txt2 = Text(box, align="right", text = "Input code again", visible=False)
txtBox_code = TextBox(box, align="left")
but= PushButton(box, command=check_cod, text = "Check the code", align="centre")

def create_app(codes, identified):
        if (identified==True):
                #app1 = App(title="Welcome Home")
                app1.display()
        else:
                #app2 = App(title="Check the code")
                app2.show()
                app2.display()
                

def main():
        recognizerFrontal = cv2.face.LBPHFaceRecognizer_create()
        recognizerFrontal.read('trainer/trainerFrontal.yml')
        pathFrontal = "lbpcascade_frontalface_improved.xml"
        detectorFrontal = cv2.CascadeClassifier(pathFrontal)
        font = cv2.FONT_HERSHEY_SIMPLEX
        recognizerLateral = cv2.face.LBPHFaceRecognizer_create()
        recognizerLateral.read('trainer/trainerLateral.yml')
        pathLateral = "lbpcascade_profileface.xml"
        detectorLateral = cv2.CascadeClassifier(pathLateral)
        id = 0
        already_sent=0
        
        f = open("UserLogin.txt", "r")
        usrs = {}
        codes = []
        for line in f:
                line = line.strip()
                split = line.split(".")
                print(split)
                usrs[int(split[0])]=split[1]
                codes.append(int(split[2]))
        f.close()

        # names related to ids: example ==> Marcelo: id=1,  etc
        #names = ['None', 'Alex', 'Paula', 'Ilza', 'Z', 'W'] 
        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video widht
        cam.set(4, 480) # set video height
        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)
        
        userIdentified = False
        totals = 0
        totals_l=0
        knowns = 0 #nr of known faces
        knowns_l=0 #nr of knowns for lateral
        unknowns_l=0 
        unknowns = 0 #number of unknown faces
        while True:
                ret, img =cam.read()
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                frontals = detectorFrontal.detectMultiScale(
                gray,
                scaleFactor = 1.3,
                minNeighbors = 8,
                minSize = (int(minW), int(minH)),
                )
                laterals = detectorLateral.detectMultiScale(
                gray,
                scaleFactor = 1.05,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
                )
                for(x,y,w,h) in frontals:
                        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                        id, confidence = recognizerFrontal.predict(gray[y:y+h,x:x+w])
                # Check if confidence is less than 100, where 0 is perfect match
                        if (confidence < 60):
                                string="a " + str(id)
                                usrName = usrs[id]
                                knowns = knowns + 1
                                confidence = " {0}%".format(round(100 - confidence))+str(id)
                        else:
                                string="b " + str(id);
                                unknowns = unknowns + 1
                                usrName = "unknown"
                                confidence = " {0}%".format(round(100 - confidence))+str(id)
                        totals = totals + 1
                        cv2.putText(img, usrName, (x+5,y-5), font, 1, (255,255,255), 2)
                        #cv2.putText(img, string, (x+5,y-100), font, 1, (255,255,255), 2)
                        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                        #cv2.putText(img, str(totals), (x+5,y+h-50), font, 1, (255,255,0), 1)
                for(x,y,w,h) in laterals:
                        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                        id, confidence = recognizerLateral.predict(gray[y:y+h,x:x+w])
                        if (confidence < 100):
                                usrName = usrs[id]
                                knowns_l = knowns_l+1
                                confidence = " {0}%".format(round(100 - confidence))
                        else:
                                usrName = "unknown"
                                unknowns_l=unknowns_l+1
                                confidence = " {0}%".format(round(100 - confidence))
                        totals_l = totals_l + 1
                        cv2.putText(img, usrName, (x+5,y-5), font, 1, (255,255,255), 2)
                        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                        #cv2.putText(img, str(totals_l), (x+5,y+h-50), font, 1, (255,255,0), 1)
                        
                put_text = 3 #Look into the camera
                if (totals%20==0):
                    if (unknowns > knowns):
                        userIdentified = False
                    else:
                        userIdentified = True
                        unknowns = 0
                        knowns = 0
                        #cv2.putText(img, "Known user logging in", (x+2, y-2), (255,255,255), 2)
                if (totals_l%20==0):
                    if (unknowns_l > knowns_l):
                        userIdentified_l = False
                    else:
                        userIdentified_l = True
                        unknowns_l = 0
                        knowns_l = 0
                #userIdentified==False #for testing purposes only
                #totals=20
                if (userIdentified==False and totals>19 and already_sent==0):
                    already_sent=1
                    cv2.putText(img, "Unknown user input code!", (x+5,y+h-25), font, 1, (255,255,0), 1)
                    pathEmail = '/home/pi/FacialRecognition/Emails'
                    dateTimeStr = datetime.datetime.now().strftime("%I:%M,%B%d,%Y")
                    cv2.imwrite(os.path.join(pathEmail, dateTimeStr+".jpg"), img)
                    sendMail()
                    create_app(codes, identified=False)
                elif (userIdentified==True and totals>19):
                    if(totals_l < 19):
                        put_text = 0
                    if(userIdentified_l == True and totals_l>19):
                        put_text = 1 #welcome home message
                if(totals>0):
                    if(put_text == 0):
                        cv2.putText(img, "Look to the right and wait", (x-200,y+h+60), font, 1, (255,255,0), 1)
                    if(put_text == 1):
                        cv2.putText(img, "Welcome home!", (x-200,y+h+60), font, 1, (255,255,0), 1)
                        #create_app(codes, identified=True)
                    if(put_text == 3):
                        cv2.putText(img, "Look into the camera", (x-200,y+h+60), font, 1, (255,255,0), 1)
                cv2.imshow('camera',img)
                k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                if k == 27:
                        break
        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and closing all connections")
        cam.release()
        cv2.destroyAllWindows()
        
        
if __name__ == "__main__":
        main()
