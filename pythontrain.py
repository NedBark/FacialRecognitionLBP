import cv2
import numpy as np
import os
import time
from PIL import Image

def main():

        detectorFrontal = cv2.CascadeClassifier("lbpcascade_frontalface_improved.xml")
        detectorLateral = cv2.CascadeClassifier("lbpcascade_profileface.xml")

        path = 'dataset'

        recognizer = cv2.face.LBPHFaceRecognizer_create()

        def getImgID(path):
                frontals = []
                ids = []
                laterals = []
                idsl = []
                imgPaths = [os.path.join(path,f) for f in os.listdir(path)]
                for imgPath in imgPaths:
                        pil = Image.open(imgPath).convert('L') 
                        img_numpy = np.array(pil, 'uint8')
                        pathSplit = os.path.split(imgPath)[-1].split(".")
                        type = str(pathSplit[1])
                        id = int(pathSplit[2])
                        if type == 'frontal':
                                frontalFaces = detectorFrontal.detectMultiScale(img_numpy)
                                for (x,y,w,h) in frontalFaces:
                                        frontals.append(img_numpy[y:y+h,x:x+w])
                                        ids.append(id)
                        if type == 'lateral':
                                lateralFaces = detectorLateral.detectMultiScale(img_numpy)
                                for (x,y,w,h) in lateralFaces:
                                        laterals.append(img_numpy[y:y+h,x:x+w])
                                        idsl.append(id)
                return frontals,ids,laterals,idsl
        [faces,ids,laterals,idsl]=getImgID(path)
        recognizer.train(faces, np.array(ids))
        recognizer.write('trainer/trainerFrontal.yml')
        recognizer.train(laterals, np.array(idsl))
        recognizer.write('trainer/trainerLateral.yml')
        print("Training is done. Success!")

