from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
from tkinter import messagebox
from final_fns import face_locations, face_encodings, compare_faces, face_distance, markAttendance
from cv2 import VideoCapture, resize, cvtColor, rectangle, putText, imshow, waitKey, COLOR_BGR2RGB, FONT_HERSHEY_SIMPLEX
import os
from pandas import read_csv
from numpy import argmin
import smtplib
from email.message import EmailMessage
from cv2 import imread, cvtColor, COLOR_BGR2RGB
from final_fns import face_locations, face_encodings
from os import listdir
import pandas as pd


windo = Tk()
windo.geometry("950x600")
#windo.geometry("1280x720")
bg = PhotoImage("backgrongimage", file = r"C:\Users\apollo\Pictures\qwer.png")
label1 = Label(windo, text=" ").grid(row=0, column=0)
label2 = Label(windo, text="Attendance System Using Face Recognition", font=('italic', 30, 'bold'), bg="cyan", padx=70,
               pady=20).grid(row=1, column=0)
label3 = Label(windo, text=" ").grid(row=2, column=0)


def browse_file():
    win = Tk()
    win.geometry("950x500")
    label1 = Label(win, text=" ").grid(row=0, column=0)
    label2 = Label(win, text="Attendance System Using Face Recognition", font=('italic', 30, 'bold'), bg="cyan",
                   padx=70,
                   pady=20).grid(row=1, column=0)
    label3 = Label(win, text=" ").grid(row=2, column=0)

    def open_file():
        top = Toplevel()
        top.title("image  window")
        top.geometry("1600x900")
        global my_image
        global file_open

        labelname = Label(top, text="Enter Name").grid(row=0, column=15)
        txt = Entry(top, width=15)
        txt.grid(column=20, row=0)

        file_open = filedialog.askopenfilename(initialdir=r"C:\Users\apollo\Pictures", title="select a file")
        my_label = Label(top, text=file_open).grid(row=0, column=0)
        my_image = ImageTk.PhotoImage(Image.open(file_open))
        my_image_label = Label(top, image=my_image).grid(row=1, column=0)
        # button inside the second window
        button_exit = Button(top, text="Exit", padx=45, pady=20, command=top.destroy, font=('italic', 20, 'bold')).grid(
            row=5,
            column=9)

        # def pop():
        #    picture = Image.open(file_open)
        #    picture = picture.save("dolls.jpg")

        def pop2():
            directory = r'C:\Users\apollo\PycharmProjects\Attendance using face recognition\img'
            img = cv2.imread(file_open)
            os.chdir(directory)
            filename = txt.get() + ".jpg"
            cv2.imwrite(filename, img)
            messagebox.showinfo('Image saved', "Face Saved")

            #saving the database
            path = r"C:\Users\apollo\PycharmProjects\Attendance using face recognition\img"
            images = []
            nameList = listdir(path)
            print(nameList)

            for img in nameList:
                curImg = imread(f'{path}/{img}')
                images.append(curImg)

            # encoding

            def findEncodings(images):
                encodedList = []
                for img in images:
                    img = cvtColor(img, COLOR_BGR2RGB)
                    # encode = face_recognition.face_encodings(img)[0]
                    camFaceLocs = face_locations(img)
                    # similarly here we are giving camFaceLocs, the face location as argument for encodings
                    encode = face_encodings(img, camFaceLocs)[0]
                    encodedList.append(encode)
                return encodedList

            encodedListKnown = findEncodings(images)


            df = pd.DataFrame(encodedListKnown)
            pathsave =  r'C:\Users\apollo\PycharmProjects\Attendance using face recognition\Encodings_db.csv'
            #probably can't take spaces between it
            df.to_csv(pathsave, sep=',')


        button_save = Button(top, text="save face", padx=45, pady=20, font=('italic', 20, 'bold'),
                             command=pop2).grid(row=0, column=9)

    # buttons on the 2nd window
    button12 = Button(win, text="BROWSE IMAGE", padx=30, pady=20, font=('italic', 20, 'bold'),
                     command=open_file).grid(
        row=3,
        column=0)

    label5 = Label(win, text=" ").grid(row=4, column=0)

    button_quit2 = Button(win, text="Exit", padx=45, pady=20, command=win.destroy, font=('italic', 20, 'bold')).grid(row=5,
                                                                                                                  column=0)

def take_attendance():
    path = r"C:\Users\apollo\PycharmProjects\Attendance using face recognition\img"
    classNames = []
    nameList = os.listdir(path)
    for img in nameList:
        classNames.append(os.path.splitext(img)[0])

    # List of encodings od known faces
    df = read_csv(r"C:\Users\apollo\PycharmProjects\Attendance using face recognition\Encodings_db.csv")
    df.drop(df.columns[[0]], axis=1, inplace=True)
    encodedListKnown = df.values.tolist()

    cap = VideoCapture(0)

    while True:  # video is a just a large no. of images
        success, img = cap.read()
        # reducing the size of image bcz its real time
        imgSmall = resize(img, (0, 0), None, 0.25, 0.25)
        imgSmall = cvtColor(imgSmall, COLOR_BGR2RGB)

        # finding the encoding of the image from the webcam:-

        # there might be multiple faces so we removed the [0] after it as then it would have only taken the first location
        camFaceLocs = face_locations(imgSmall)
        # similarly here we are giving camFaceLocs, the face location as argument for encodings
        camFaceEncodings = face_encodings(imgSmall, camFaceLocs)

        # finding the matches
        # first we will iterate through all the faces found in the cam
        for encodeFace, faceLoc in zip(camFaceEncodings, camFaceLocs):
            matches = compare_faces(encodedListKnown, encodeFace)
            faceDist = face_distance(encodedListKnown, encodeFace)
            # it will give us the values for all the faces from the list, lowest distance will be the best match
            # print(faceDist)
            matchIndex = argmin(faceDist)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)
                # to show box in webcam with name
                y1, x2, y2, x1 = faceLoc
                # multiplying the location coordinates by 4 bcz be derived them for scaled down image
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # addition box for name space
                rectangle(img, (x1, y1 - 35), (x2, y2), (0, 255, 0))
                # name as text
                putText(img, name, (x1 + 6, y2 - 6), FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                # calling the func
                markAttendance(name)

        # to show webcam images
        imshow('Taking Attendance // Press Q to QUIT', img)
        waitKey(1)
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()



def showattendance():
    df = pd.read_csv("Attendance.csv")
    print(df)

def mailattendance():
    winter = Tk()
    winter.geometry("950x500")
    label1 = Label(winter, text=" ").grid(row=0, column=0)
    label2 = Label(winter, text="Attendance System Using Face Recognition", font=('italic', 30, 'bold'), bg="cyan",
                   padx=70,
                   pady=20).grid(row=1, column=0)
    label3 = Label(winter, text=" ").grid(row=2, column=0)

    SENDER_EMAIL = "projectminor705@gmail.com"
    APP_PASSWORD = "minorproject@123"

    F = open(r'C:\Users\apollo\PycharmProjects\Attendance using face recognition\email'
             '.txt', mode='r')  # enter your file path here
    text = F.readline()
    recipient_email = text.split(",")

    #recipient_email = str(txt.get())
    content = "henlo 2"
    subject = "Attendance List"
    excel_file = r'C:\Users\apollo\PycharmProjects\Attendance using face recognition\Attendance.csv'

    def send_mail():

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg.set_content(content)

        with open(excel_file, 'rb') as f:
            file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=excel_file)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.ehlo()
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.ehlo()
            smtp.send_message(msg)
            smtp.ehlo()
            smtp.quit()


    # buttons on the 2nd window
    button12 = Button(winter, text="mail", padx=30, pady=20, font=('italic', 20, 'bold'),
                      command=send_mail).grid(
        row=5,
        column=0)

    label5 = Label(winter, text=" ").grid(row=6, column=0)

    button_quit2 = Button(winter, text="Exit", padx=45, pady=20, command=winter.destroy, font=('italic', 20, 'bold')).grid(
        row=7,
        column=0)





#buttons on the first window
button1 = Button(windo, text="Add New Student", padx=30, pady=20, font=('italic', 20, 'bold'), command=browse_file).grid(
        row=3,
        column=0)

label5 = Label(windo, text=" ").grid(row=4, column=0)
button11 = Button(windo, text="Take Attendance", padx=30, pady=20, font=('italic', 20, 'bold'), command=take_attendance).grid(
        row=5,
        column=0)

label51 = Label(windo, text=" ").grid(row=6, column=0)
button1e = Button(windo, text="Mail The Attendance", padx=30, pady=20, font=('italic', 20, 'bold'),
                  command=mailattendance).grid(
        row=7,
        column=0)

label5e = Label(windo, text=" ").grid(row=8, column=0)

button_quit = Button(text="Exit", padx=45, pady=20, command=windo.destroy, font=('italic', 20, 'bold')).grid(row=9, column=0)






windo.mainloop()
