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
account_sid = "AC38e936344a9907075de11ecb56d452c4"
auth_token = "72c7a910c635f319c7bbf7ca494ffcc0"

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
    ##keyboard = np.zeros((600, 1000, 3), np.uint8)
    keyboard = np.zeros((1000, 800, 3), np.uint8)


    keys_set_1 = {0: "1", 1: "2", 2: "3",
                  3: "4",4: "5", 5: "6",
                  6: "7", 7: "9",8: "3",
                  9: "8", 10: "9",11:"0",12:"2"}



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
    ##    elif letter_index == 13:
    ##        x = 600
    ##        y = 400
    ##    elif letter_index == 14:
    ##        x = 800
    ##        y = 400

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
    ##    cv2.line(keyboard, (int(cols/2) - int(th_lines/2), 0),(int(cols/2) - int(th_lines/2), rows),
    ##             (51, 51, 51), th_lines)
        ## cv2.putText(keyboard, "PASSword", (80, 300), font, 6, (255, 255, 255), 5)
    ##    cv2.putText(keyboard, "RIGHT", (80 + int(cols/2), 300), font, 6, (255, 255, 255), 5)

    def midpoint(p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

    ##font = cv2.FONT_HERSHEY_PLAIN

    def get_blinking_ratio(eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    ##    hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    ##    ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

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

    pf =['3','4']

    while True:


      while True :

     
        _, frame = cap.read()
        #frame = cv2.resize(frame, None, fx=0.8, fy=0.8)
        rows, cols, _ = frame.shape
    ##    keyboard[:] = (26, 26, 26)
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
    ##    else:
    ##        keys_set = keys_set_2
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
    ##            else:
    ##                keyboard_selected = "left"
    ##                keyboard_selection_frames += 1
    ##                # If Kept gaze on one side more than 15 frames, move to keyboard
    ##                if keyboard_selection_frames == 15:
    ##                    select_keyboard_menu = False
    ####                    left_sound.play()
    ##                    # Set frames count to 0 when keyboard selected
    ##                    frames = 0
    ##                if keyboard_selected != last_keyboard_selected:
    ##                    last_keyboard_selected = keyboard_selected
    ##                    keyboard_selection_frames = 0

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
                        if active_letter != "E" and active_letter != "C":
                            count=count+1
                            text += active_letter
                            text1.append(active_letter)
                            print('text1 {}'.format(text1))
                        if active_letter == "E" or active_letter == "C" :
                            text += " "
                            del text1[-1]
                            count=count-1
                            text1.pop(count)
                            count=count-1
                            text1.pop(count)
                            print('del {}'.format(text1))
                            print(active_letter)
                        text += " "
                        print(text)
                        if len(text1) ==2 :
                            print('Enter password')
                            print(type(str(text1)))

                            if text1 == pf:
                                text += " "
                                playsound("pass.mp3")
                                print('password matched')
                                name="password matched"
                                cv2.putText(frame, name, (x, y + h), cv2.FONT_HERSHEY_COMPLEX, 16, (0, 255, 0), 2)
                                time.sleep(8)
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
            if letter_index == 11:
                letter_index = 0
            for i in range(11):
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
    ##    cv2.imshow("Board", board)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ##    key = cv2.waitKey(1)
    ##    if key == 27:
    ##        break

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
                Id = "sush"
                print("sush")
                #lecture=1
                sample=0
            cam.release()
            cv2.destroyAllWindows()
            eye()
                 
##                 
                  

                                      
                 
              
        else:
            count=count+1

        if count > 20:
            count=0
            #print(Id)
            mon=0
            Id = "unknown"
            print('UNKNOWN ')
            client.api.account.messages.create(
    to="+91-6360137895",
    from_="+13602343600" ,  #+1 210-762-4855"#14804852511
    body=" Unkown person Detected")

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
