import face_recognition
import os
import cv2
import numpy as np
from datetime import datetime
import keyboard

path="ImagesAttendance"
images=[] #img to numpy array
classNames=[] #stores people's namesz
mylist=os.listdir(path) #lists all the images in dir
savedImg=[]
print(mylist)

# accessing images in folder
for cl in mylist:
    curImg=cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0]) #root path of name [0] ext path [1]

print(classNames)

# return the 128-dimension face encoding for each face in the image.
# A face encoding is basically a way to represent the face using a set of 128 computer-generated measurements.
# Two different pictures of the same person would have similar encoding and two different people would have totally different encoding
def find_encodings(images):
    encodeList=[]
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodeList.append(encode)
    return encodeList

def save_img(imagesz,nami):
    savedImg=os.listdir(r"C:\Users\Musadiq Pasha K\Desktop\#Face Me\only_name")
    if nami not in savedImg:
        cv2.imwrite(fr"C:\Users\Musadiq Pasha K\Desktop\#Face Me\only_name\{nami}.jpg", imagesz)

def markAttendance(name):
    print(name, "attended")
    with open("Attendance.txt",'r+') as f:
        myDataList = f.readlines() #reads every line in attendance list
        nameList = []  # used to store name's of people who already attended
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])#name 0 , 1 time

        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%I:%M %p") # I - 12 hr format() , minute , pm or am
            f.writelines(f'\n{name},{dtString}') # writes time
            #print(name,"attended")

encodeListKnown = find_encodings(images)
print("Encoding Completed..")

cap = cv2.VideoCapture(0) # starts video capture through webcam

while True:
    #img = numpy array  ,  succces= if loaded or not
    success,img =cap.read()
    # we resizze to 1/4th of size of ease of calculation and faster read time
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    #no of faces in an frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    # displays a text below                         no               co ordi where tot          font                colour    size
    cv2.putText(img,f'Number of faces detected: {len(facesCurFrame)}', (100, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    #main shittt
    for encodeFace,FaceLoc in zip(encodesCurFrame,facesCurFrame) :
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace,tolerance=0.5) # lower is more strict
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis) # gives matchIndex of match name out of all images

        if matches[matchIndex]:
            name = classNames[matchIndex].upper() # Capitalizes each word
            #print(name)
            # FaceLoc = up right down left
            y1,x2,y2,x1=FaceLoc
            # multiply by 4 cuz we decresed the size by 4
            # were drwaing on regular image not of reduced size one
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4

            # draw's rectangle img , loc , colour , size
            cv2.rectangle(img, (x1,y1),(x2,y2) ,(255, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2),(255, 255, 0), cv2.FILLED)
            # displays name
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
            # save img
            save_img(img, name)

            # call's attendace to add name
            markAttendance(name)

        else:
                name = "unknown"
                # FaceLoc = up right down left
                y1, x2, y2, x1 = FaceLoc
                # multiply by 4 cuz we decresed the size by 4
                # were drwaing on regular image not of reduced size one
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                # draw's rectangle img , loc , colour , size
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 0), cv2.FILLED)
                # displays name
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

    # continouly displays the image
    cv2.imshow('webcam',img)
    cv2.waitKey(1)

    if keyboard.is_pressed('q'):
        print("i quit!!")
        break