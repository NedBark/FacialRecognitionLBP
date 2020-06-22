import cv2
import numpy as np
import os
from PIL import Image
import time


def main(personID, usr, code):
        exists=0 #variable to check if the user already exists
        f = open ("UserLogin.txt", "r")
        for line in f:
                line = line.strip("\n")
                string = line.split(".")
                if (personID == int(string[0]) and usr==string[1]):
                        exists=1
        
        cam = cv2.VideoCapture(0) #captures the first available camera, Pi cam
        #or first USB one found
        cam.set(3, 640) #set width
        cam.set(4, 480) #set height

        font = cv2.FONT_HERSHEY_SIMPLEX

        frontalDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        #lateralDetector = cv2.CascadeClassifier('haarcascade_profileface.xml')
        lateralDetector = cv2.CascadeClassifier('lbpcascade_profileface.xml')

        c=0
        l=0

        samples = 20

        while(True):
                ret, image=cam.read()
                #img=cv2.flip(img,-1) #We might need to flip the immage depending on the camera
                grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                faces = frontalDetector.detectMultiScale(grayImage,1.3,6)
                laterals = lateralDetector.detectMultiScale(grayImage,1.2,6)
                if c<samples:
                        cv2.putText(image, "Look at the camera, wait for 20 pictures: "+ str(c), (0,25), font, 0.5, (255,255,255), 2)
                        for(x,y,w,h) in faces:
                                c = c+1
                                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                                cv2.imwrite("dataset/"+usr+".frontal." + str(personID) + '.' + str(c) + '.jpg', grayImage[y:y+h,x:x+w]) #x,y are top left
                                cv2.imshow('image', image)
                if c==samples-1:
                        cv2.putText(image, "Now turn your head around to capture lateral faces: "+ str(l), (0,25), font, 0.5, (255,255,255), 2)
                if l<samples:
                        for(x,y,w,h) in laterals:
                                l=l+1
                                cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
                                cv2.imwrite("dataset/"+usr+".lateral." + str(personID) + '.' + str(l) + ".jpg", grayImage[y:y+h,x:x+w])
                                cv2.imshow('image', image)
                esc = cv2.waitKey(100) & 0xff
                if esc == 27:
                        break
                elif c >=samples and l>=samples:
                        if(exists==0):
                                f = open("UserLogin.txt", "a")
                                f.write(str(personID)+".")
                                f.write(usr+"."+str(code)+"\n")
                                #f.write(str(2)+"."+"TudorVianu\n")
                                f.close()
                                print("Acquiring faces terminated with success, closing...")
                                time.sleep(1)
                                break
                        print("Acquiring faces terminated with success, closing...")
                        break

        cam.release()
        cv2.destroyAllWindows()

if __name__=="__main()__":
        main()
