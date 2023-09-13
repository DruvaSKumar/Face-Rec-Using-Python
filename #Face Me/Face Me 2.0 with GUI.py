import face_recognition
import numpy as np
from datetime import datetime
import os
import cv2
import keyboard
import pyautogui
import customtkinter as cstk
import tkinter as tk

# GUIIIII
cstk.set_appearance_mode("dark")
cstk.set_default_color_theme("green")
root = cstk.CTk()
root.geometry("1920x1080")
root.title("Facial Recognition System")

# create the needed variables
path = "ImagesAttendance"
images = []  #  img to numpy array
image_names = []  #stores people's namesz
mylist = os.listdir(path)  #lists all the images in dir
savedImg = []
print(mylist)

# accessing images in folder


def access():
    global images,image_names
    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        image_names.append(os.path.splitext(cl)[0]) #root path of name [0] ext path [1]
    print(image_names)


# return the 128-dimension face encoding for each face in the image.
# A face encoding is basically a way to represent the face using a set of 128 computer-generated measurements.
# Two different pictures of the same person would have similar encoding and two different people would have totally different encoding

def find_encodings(images):
    global encodeList
    encodeList=[]
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodeList.append(encode)
    return encodeList

# to save the captured image
def save_img(imagesz,nami):
    savedImg=os.listdir(r"C:\Users\Musadiq Pasha K\Desktop\#Face Me\only_name")
    if nami not in savedImg:
        cv2.imwrite(fr"C:\Users\Musadiq Pasha K\Desktop\#Face Me\only_name\{nami}.jpg", imagesz)


# to mark the attendace into txt file for a new name
def markAttendance(name):
    print(name, "attended")
    with open("Attendance.txt",'r+') as f:
        myDataList = f.readlines() #reads every line in attendance list
        nameList = []  # used to store name's of people who already attended
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])  #name 0 , 1 time

        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%I:%M %p") # I - 12 hr format() , minute , pm or am
            f.writelines(f'\n{name},{dtString}') # writes time


def webcam_scan():
    cap = cv2.VideoCapture(0) # starts video capture through webcam

    while True:
        #img = numpy array  ,  succces= if loaded or not
        success,img = cap.read()
        # we resizze to 1/4th of size of ease of calculation and faster read time
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        #no of faces in an frame
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

        # displays a text below                         no               co ordi where tot          font                colour    size
        cv2.putText(img,f'Number of faces detected: {len(facesCurFrame)}', (100, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

        #main shittt
        for encodeFace,FaceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace,tolerance=0.5) # lower is more strict
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            matchIndex = np.argmin(faceDis) # gives matchIndex of match name out of all images

            if matches[matchIndex]:
                name = image_names[matchIndex].upper() # Capitalizes each word
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
            cv2.destroyWindow('webcam')
            break


def take_new_pic():
    new_name = pyautogui.prompt('What is your name?',title="Name",default="new_image")
    new_name+=".jpg"
    tk.messagebox.showinfo("Alert", "Look at the Camera in 3 sec !")
    result, new_img = cv2.VideoCapture(0).read()
    cv2.imwrite(rf"C:\Users\Musadiq Pasha K\Desktop\#Face Me\ImagesAttendance\{new_name}",new_img)
    cv2.imshow("New Image",new_img)
    cv2.waitKey(0)
    cv2.destroyWindow('New Image')
    images.append(cv2.imread(fr'C:\Users\Musadiq Pasha K\Desktop\#Face Me\ImagesAttendance\{new_name}'))
    image_names.append(os.path.splitext(new_name)[0])
    print(os.path.splitext(new_name)[0])
    encodeList.append(face_recognition.face_encodings(images[-1])[0])

#open attendance file


def attendance():
    os.startfile(r"C:\Users\Musadiq Pasha K\Desktop\#Face Me\Attendance.txt")


def show():
    os.startfile(r"C:\Users\Musadiq Pasha K\Desktop\#Face Me\only_name")


def know_faces():
    os.startfile(r"C:\Users\Musadiq Pasha K\Desktop\#Face Me\ImagesAttendance")


def about():
    os.startfile(r"C:\Users\Musadiq Pasha K\Desktop\#Face Me\ABOUT OURSELVES.png")

###################################
access()# get the names of images
encodeListKnown = find_encodings(images) # encode all the images
print("Encoding Completed..")

#GUIIIII
imag = tk.PhotoImage(file="Brain_Circuit_Encoding.png",)

frame = cstk.CTkFrame(master=root)
frame.pack(padx=60,pady=20,fill="both",expand=True)

label = cstk.CTkLabel(master=frame,text="Facial Recognition System",font=("Roboto",24),compound="left")
label.pack(pady=12,padx=10)

bglabel = cstk.CTkLabel(master=frame,image=imag, width=1080,height=1080)
bglabel.pack()

button1 = cstk.CTkButton(master=frame,text="Scan face (Webcam)",command=webcam_scan,height=80,width=265,font=("Arial",24))
button1.place(relx=0.3,rely=0.3,anchor="e")

button4 = cstk.CTkButton(master=frame,text="Add a new face",command=take_new_pic,height=90,width=250,font=("Arial",24))
button4.place(relx=0.75,rely=0.3,anchor="w")

button5 = cstk.CTkButton(master=frame,text="Show Scanned Images",command=show,height=90,width=150,font=("Arial",24))
button5.place(relx=0.3,rely=0.57,anchor="e")

button6 = cstk.CTkButton(master=frame,text="Known Faces",command=know_faces,height=90,width=250,font=("Arial",24))
button6.place(relx=0.75,rely=0.562,anchor="w")

button3 = cstk.CTkButton(master=frame,text="Open Attendance",command=attendance,height=80,width=230,font=("Arial",24))
button3.place(relx=0.3,rely=0.85,anchor="e")

button2 = cstk.CTkButton(master=frame,text="About",command=about,height=90,width=250,font=("Arial",24))
button2.place(relx=0.75,rely=0.85,anchor="w")

root.mainloop()

