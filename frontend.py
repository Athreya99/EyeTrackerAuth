from tkinter import *
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from tkinter import *
import os
import sys
from PIL import Image, ImageTk
import time
import tkinter

window = tk.Tk()
window.title("eye tracker")
window.geometry('1000x1000')
##window.configure(background ="light green")

ima = PhotoImage(file = r'C:\\Users\\athre\\Desktop\\Raspberry-Face-Recognition-master\\a.png')
label = tk.Label(window, image = ima)

lb1=tk.Label(window, text="WELCOME ",width=10,font=("Century Gothic",30,"bold","italic"),foreground="black",bg="sky blue")
lb1.place(x=300,y=80)

def fun():
    # Import OpenCV2 for image processing
    import cv2
    import time
    # Start capturing video
    vid_cam = cv2.VideoCapture(0)

    # Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    # For each person, one face id
    face_id = 2 # for multiple person different ids

    # Initialize sample face image
    count = 0

    # Start looping
    while(True):

        # Capture video frame
        _, image_frame = vid_cam.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        # Detect frames of different sizes, list of faces rectangles
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # Loops for each faces
        for (x,y,w,h) in faces:

            # Crop the image frame into rectangle
            cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)

            # Increment sample face image
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            # Display the video frame, with bounded rectangle on the person's face
            cv2.imshow('Frame', image_frame)

        # To stop taking video, press 'q' for at least 100ms
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        # If image taken reach 100, stop taking video
        elif count>50:
            break

    # Stop video
    vid_cam.release()

    # Close all started windows
    cv2.destroyAllWindows()

    ##    os.system("python face_datasets.py")

def fun1():
    import cv2
    # Import os for file path
    import cv2, os

    # Import numpy for matrix calculation
    import numpy as np

    # Import Python Image Library (PIL)
    from PIL import Image

    # Create Local Binary Patterns Histograms for face recognization

    recognizer = cv2.face.LBPHFaceRecognizer_create()


    # Using prebuilt frontal face training model, for face detection
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

    # Create method to get the images and label data
    def getImagesAndLabels(path):

        # Get all file path
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

        # Initialize empty face sample
        faceSamples=[]

        # Initialize empty id
        ids = []

        # Loop all the file path
        for imagePath in imagePaths:

            # Get the image and convert it to grayscale
            PIL_img = Image.open(imagePath).convert('L')

            # PIL image to numpy array
            img_numpy = np.array(PIL_img,'uint8')

            # Get the image id
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            print(id)

            # Get the face from the training images
            faces = detector.detectMultiScale(img_numpy)

            # Loop for each face, append to their respective ID
            for (x,y,w,h) in faces:

                # Add the image to face samples
                faceSamples.append(img_numpy[y:y+h,x:x+w])

                # Add the ID to IDs
                ids.append(id)

        # Pass the face array and IDs array
        return faceSamples,ids

    # Get the faces and IDs
    faces,ids = getImagesAndLabels('dataset')

    # Train the model using the faces and IDs
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer.yml
    recognizer.write('trainer/trainer.yml')

    ##    os.system("python training.py")


def fun2():
    # Import OpenCV2 for image processing
    import cv2
    import os

    import numpy as np
    import time

    import dlib
    from math import hypot
    import time
    import os
    from playsound import playsound
    from twilio.rest import Client

    # Find these values at https://twilio.com/user/account
    account_sid = "AC1ce26e0baf27085ed2dfed1768f4c78e"
    auth_token = "248d7880336d4f29932c876b64d05716"

    client = Client(account_sid, auth_token)


    # Create Local Binary Patterns Histograms for face recognization

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load the trained mode
    recognizer.read('trainer/trainer.yml')

    # Load prebuilt model for Frontal Face
    cascadePath = "haarcascade_frontalface_default.xml"

    # Create classifier from prebuilt model
    faceCascade = cv2.CascadeClassifier(cascadePath);

    # Set the font style
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize and start the video frame capture
    cam = cv2.VideoCapture(0)

    # Local variable Declaration
    count=0
    count1=0
    count2=0
    count3=0
    count4=0
    sample=0
    take=1

    def eye():
        cap = cv2.VideoCapture(0)

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        # Keyboard settings
        #keyboard = np.zeros((600, 1000, 3), np.uint8)
        # keyboard = np.zeros((1000, 800, 3), np.uint8)
        #
        #
        # keys_set_1 = {0: "1", 1: "2", 2: "3",
        #               3: "4",4: "5", 5: "6",
        #               6: "7", 7: "9",8: "3",
        #               9: "8", 10: "9",11:"0",12:"2"}

        keyboard = np.zeros((600, 1000, 3), np.uint8)
        keys_set_1 = {0: " ", 1: "0", 2: " ", 3: "1", 4: " ", 5: "2", 6: " ", 7: "3", 8: " ", 9: "4",
                      10: " ", 11: " ", 12: " ", 13: " ", 14: "<"}
        keys_set_2 = {0: " ", 1: "5", 2: " ", 3: "6", 4: " ",5: "7", 6: " ", 7: "8", 8: " ", 9: "9",
                      10: " ", 11: " ", 12: " ", 13: " ", 14: "<"}




        def draw_letters(letter_index, text, letter_light):
            # Keys
            if letter_index == 0:
                x = 0
                y = 0
            elif letter_index == 1:
                x = 200
                y = 0
            elif letter_index == 2:
                x = 400
                y = 0
            elif letter_index == 3:
                x = 600
                y = 0
            elif letter_index == 4:
                x = 0
                y = 200
            elif letter_index == 5:
                x = 200
                y = 200
            elif letter_index == 6:
                x = 400
                y = 200
            elif letter_index == 7:
                x = 600
                y = 200
            elif letter_index == 8:
                x = 0
                y = 400
            elif letter_index == 9:
                x = 200
                y = 400
            elif letter_index == 10:
                x = 400
                y = 400
            elif letter_index == 11:
                x = 600
                y = 400
            elif letter_index == 12:
               x = 0
               y = 600
            elif letter_index == 13:
               x = 600
               y = 400
            elif letter_index == 14:
               x = 800
               y = 400

            width = 200
            height = 200
            th = 3 # thickness

            # Text settings
            font_letter = cv2.FONT_HERSHEY_PLAIN
            font_scale = 9
            font_th = 4
            text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
            width_text, height_text = text_size[0], text_size[1]
            text_x = int((width - width_text) / 2) + x
            text_y = int((height + height_text) / 2) + y

            if letter_light is True:
                cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
                cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
            else:
                cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
                cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)

        def draw_menu():
            rows, cols, _ = keyboard.shape
            th_lines = 4 # thickness lines
            cv2.line(keyboard, (int(cols/2) - int(th_lines/2), 0),(int(cols/2) - int(th_lines/2), rows),
                    (51, 51, 51), th_lines)
            cv2.putText(keyboard, "LEFT", (80, 300), font, 6, (255, 255, 255), 5)
            cv2.putText(keyboard, "RIGHT", (80 + int(cols/2), 300), font, 6, (255, 255, 255), 5)

        def midpoint(p1 ,p2):
            return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

        font = cv2.FONT_HERSHEY_PLAIN

        def get_blinking_ratio(eye_points, facial_landmarks):
            left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
            right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
            center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
            center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

           # hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
           # ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)


            hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
            ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

            ratio = hor_line_lenght / ver_line_lenght
            return ratio

        def eyes_contour_points(facial_landmarks):
            left_eye = []
            right_eye = []
            for n in range(36, 42):
                x = facial_landmarks.part(n).x
                y = facial_landmarks.part(n).y
                left_eye.append([x, y])
            for n in range(42, 48):
                x = facial_landmarks.part(n).x
                y = facial_landmarks.part(n).y
                right_eye.append([x, y])
            left_eye = np.array(left_eye, np.int32)
            right_eye = np.array(right_eye, np.int32)
            return left_eye, right_eye

        def get_gaze_ratio(eye_points, facial_landmarks):
            left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                        (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                        (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                        (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                        (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                        (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
            # cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)

            height, width, _ = frame.shape
            mask = np.zeros((height, width), np.uint8)
            cv2.polylines(mask, [left_eye_region], True, 255, 2)
            cv2.fillPoly(mask, [left_eye_region], 255)
            eye = cv2.bitwise_and(gray, gray, mask=mask)

            min_x = np.min(left_eye_region[:, 0])
            max_x = np.max(left_eye_region[:, 0])
            min_y = np.min(left_eye_region[:, 1])
            max_y = np.max(left_eye_region[:, 1])

            gray_eye = eye[min_y: max_y, min_x: max_x]
            _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
            height, width = threshold_eye.shape
            left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
            left_side_white = cv2.countNonZero(left_side_threshold)

            right_side_threshold = threshold_eye[0: height, int(width / 2): width]
            right_side_white = cv2.countNonZero(right_side_threshold)

            if left_side_white == 0:
                gaze_ratio = 1
            elif right_side_white == 0:
                gaze_ratio = 5
            else:
                gaze_ratio = left_side_white / right_side_white
            return gaze_ratio

        # Counters
        frames = 0
        letter_index = 0
        blinking_frames = 0
        frames_to_blink = 6
        frames_active_letter = 9

        # Text and keyboard settings
        text = ""
        text1=[]
        keyboard_selected = "left"
        last_keyboard_selected = "left"
        select_keyboard_menu = True
        keyboard_selection_frames = 0
        count=0
        pf =[]

        pf =['1','2','3','4']

        while True:


          while True :
            _, frame = cap.read()
            #frame = cv2.resize(frame, None, fx=0.8, fy=0.8)
            rows, cols, _ = frame.shape
           # keyboard[:] = (26, 26, 26)
            keyboard[:] = (26, 26, 26)
            frames += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Draw a white space for loading bar
            frame[rows - 50: rows, 0: cols] = (255, 255, 255)

            if select_keyboard_menu is True:
                draw_menu()

            # Keyboard selected
            if keyboard_selected == "left":
                keys_set = keys_set_1
            else:
               keys_set = keys_set_2
            active_letter = keys_set[letter_index]

            # Face detection
            faces = detector(gray)
            for face in faces:
                landmarks = predictor(gray, face)

                left_eye, right_eye = eyes_contour_points(landmarks)

                # Detect blinking
                left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
                right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
                blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

                # Eyes color
                cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
                cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)


                if select_keyboard_menu is True:
                    # Detecting gaze to select Left or Right keybaord
                    gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
                    gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
                    gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
                    print(gaze_ratio)

                    if gaze_ratio <= 5:
                        keyboard_selected = "right"
                        keyboard_selection_frames += 1
                        # If Kept gaze on one side more than 15 frames, move to keyboard
                        if keyboard_selection_frames == 15:
                            select_keyboard_menu = False
        ##                    right_sound.play()
                            # Set frames count to 0 when keyboard selected
                            frames = 0
                            keyboard_selection_frames = 0
                        if keyboard_selected != last_keyboard_selected:
                            last_keyboard_selected = keyboard_selected
                            keyboard_selection_frames = 0
                    else:
                        keyboard_selected = "left"
                        keyboard_selection_frames += 1
                       # If Kept gaze on one side more than 15 frames, move to keyboard
                        if keyboard_selection_frames == 15:
                            select_keyboard_menu = False
        ##                    left_sound.play()
                           # Set frames count to 0 when keyboard selected
                            frames = 0
                        if keyboard_selected != last_keyboard_selected:
                            last_keyboard_selected = keyboard_selected
                            keyboard_selection_frames = 0

                else:
                    # Detect the blinking to select the key that is lighting up
                    if blinking_ratio > 5:
                        # cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0), thickness=3)
                        blinking_frames += 1
                        frames -= 1

                        # Show green eyes when closed
                        cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                        cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

                        # Typing letter
                        if blinking_frames == frames_to_blink:
                            if active_letter != "<" and active_letter != "_":
                                count=count+1
                                text += active_letter
                                text1.append(active_letter)
                                print('text1 {}'.format(text1))
                            if active_letter == "<" :
                                text += " "
                                del text1[-1]
                                count=count-1
                                text1.pop(count)
                                print('del {}'.format(text1))
                                print(active_letter)
                            text += " "
                            print(text)
                            if len(text1) ==4 :
                                print('Enter password')
                                print(type(str(text1)))

                                if text1 == pf:
                                    text += " "
                                    playsound("pass.mp3")
                                    print('password matched')
                                    name="password matched"
                                    cv2.putText(frame, name, (x, y + h), cv2.FONT_HERSHEY_COMPLEX, 16, (0, 255, 0), 2)
                                    time.sleep(0.5)
    ##

                                    text1=[]
                                    count=0
                                    once =1
    ##                                cap.release()
        ##                            pf = Rfid_scanner()
                                else:
                                    print('not matched ')
                                    text1=[]
                                    count=0
        ##                        if text == 'AZ':
        ##                            print('password matches ')
        ##                    sound.play()
                            select_keyboard_menu = True
                            # time.sleep(1)

                    else:
                        blinking_frames = 0


            # Display letters on the keyboard
            if select_keyboard_menu is False:
                if frames == frames_active_letter:
                    letter_index += 1
                    frames = 0
                if letter_index == 15:
                    letter_index = 0
                for i in range(15):
                    if i == letter_index:
                        light = True
                    else:
                        light = False
                    draw_letters(i, keys_set[i], light)


            # Blinking loading bar
            percentage_blinking = blinking_frames / frames_to_blink
            loading_x = int(cols * percentage_blinking)
            cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)


            cv2.imshow("Frame", frame)
            cv2.imshow("Virtual keyboard", keyboard)
            time.sleep(0.2)
        ##    cv2.imshow("Board", board)

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            key = cv2.waitKey(1)
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


        # Loop
    while True:

        # Read the video frame
        ret, im =cam.read()

        # Convert the captured frame into grayscale
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

        # Get all face from the video frame
        faces = faceCascade.detectMultiScale(gray, 1.2,5)

        # For each face in faces
        for(x,y,w,h) in faces:

            # Create rectangle around the face
            cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)

            # Recognize the face belongs to which ID
            Id,i= recognizer.predict(gray[y:y+h,x:x+w])

            #print(i)
           # print(Id)

            if i < 60:
                sample= sample+1
                if Id == 2 :
                    count1=1
                    Id = "user1"
                    print("user1")
                    client.api.account.messages.create(
    to="+917259716899",
    from_="+19418456528" ,  #+1 210-762-4855"#14804852511
    body="1234")
                    #lecture=1
                    sample=0
                cam.release()
                cv2.destroyAllWindows()
                eye()

            else:
                count=count+1

            if count > 20:
                count=0
                #print(Id)
                mon=0
                Id = "unknown"
                print('UNKNOWN ')
                client.api.account.messages.create(
        to="+918792840240",
        from_="+19418456528" ,  #+1 210-762-4855"#14804852511
        body=" 1234")

                #os.system('python,gaze-copy.py')



            # Put text describe who is in the picture
            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
            cv2.putText(im, str(Id), (x,y-40), font, 2, (255,255,255), 3)
            #os.system('python,gaze-copy.py')

        # Display the video frame with the bounded rectangle
        cv2.imshow('im',im)

        # If 'q' is pressed, close program
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

            if sample > 50:
                sample =0


    # Stop the camera
    cam.release()

    # Close all windows
    cv2.destroyAllWindows()


def click():


    window = tk.Toplevel()
    window.title("Welcome")
    window.geometry('1920x1080')
##    window.configure(background ="brown")


    ima = PhotoImage(file = 'C:\\Users\\athre\\Desktop\\Raspberry-Face-Recognition-master\\a.png')
    label = ttk.Label(window, image = ima)

    lb1=tk.Label(window, text="Eye Tracking",width=50,font=("Century Gothic",26,"bold","italic"),foreground="white",bg="black")
    lb1.place(x=300,y=80)


    button1=Button(window,text="face Capturing",command=fun,width=20,font=("Century Gothic",24,"bold","italic"),foreground="white",bg="black")
    button1.place(x=100,y=300)

    button1=Button(window,text="Traing faceid",command=fun1,width=20,font=("Century Gothic",24,"bold","italic"),foreground="white",bg="black")
    button1.place(x=500,y=300)

    button1=Button(window,text="Face Recognition & password Detection",command=fun2,width=45,font=("Century Gothic",24,"bold","italic"),foreground="white",bg="black")
    button1.place(x=100,y=500)

    button1=Button(window,text="Quit",command=window.destroy,width=10,font=("Century Gothic",24,"bold","italic"),foreground="white",bg="black")
    button1.place(x=1000,y=500)


    label.pack()
    window.mainloop()


btn=tk.Button(window, text="Click Here",command=click,width=10,height=1,font=("Century Gothic",24,"bold"),foreground="black",bg="sky blue")
btn.place(x=980,y=250)
label.pack()
window.mainloop()
