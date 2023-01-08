import cv2
import mediapipe as mp
import pyautogui as pa
import time


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

wrist = mpHands.HandLandmark.WRIST
thumb_tip, thumb_mcp = mpHands.HandLandmark.THUMB_TIP, mpHands.HandLandmark.THUMB_MCP
index_tip, index_mcp = mpHands.HandLandmark.INDEX_FINGER_TIP, mpHands.HandLandmark.INDEX_FINGER_MCP
mid_tip, mid_mcp = mpHands.HandLandmark.MIDDLE_FINGER_TIP, mpHands.HandLandmark.MIDDLE_FINGER_MCP
ring_tip, ring_mcp = mpHands.HandLandmark.RING_FINGER_TIP, mpHands.HandLandmark.RING_FINGER_MCP
pinky_tip, pinky_mcp = mpHands.HandLandmark.PINKY_TIP, mpHands.HandLandmark.PINKY_MCP

fingertips = [thumb_tip, index_tip, mid_tip, ring_tip, pinky_tip]
midpoints = [thumb_mcp, index_mcp, mid_mcp, ring_mcp, pinky_mcp]
keypoints = [wrist, thumb_tip, thumb_mcp, index_tip, index_mcp, mid_tip, mid_mcp, ring_tip, ring_mcp, pinky_tip, pinky_mcp]
gesture = None

def draw_hands():
    if results.multi_hand_landmarks: # checking for any results in the camera frame
        for handLms in results.multi_hand_landmarks:  # working with each hand
            for id, lm in enumerate(handLms.landmark):
                if id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                    h, w, c = image.shape  # height, width, channel
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(image, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                elif id == 0 or id == 3 or id == 6 or id == 10 or id == 14 or id == 18:
                    h, w, c = image.shape  # height, width, channel
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(image, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

def gestures():
    if results.multi_hand_landmarks:  # checking for any results in the camera frame
        for id, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hlm = hand_landmarks.landmark  # variable to shorten function
            for i in keypoints:
                print(f'{mpHands.HandLandmark(i).name}')
                x = hlm[i.value].x  # find x value of landmark
                y = hlm[i.value].y  # find y value of landmark
                print("x =", x, "y =", y)
                if hlm[thumb_mcp].y > hlm[thumb_tip].y:
                    print("Thumbs up")
                    #pa.press("PgUp")
                if hlm[thumb_mcp].y < hlm[thumb_tip].y:
                    print("Thumbs down")
                    #pa.press("PgDn")
                if hlm[thumb_tip].y > hlm[index_tip].y < hlm[index_mcp].y and hlm[thumb_mcp].x > hlm[thumb_tip].x:
                    print("take the L")

# main program
cap = cv2.VideoCapture(0)  # get webcam feed
while True:

    success, image = cap.read()  # read the frames from the camera
    image = cv2.flip(image, 1)  # flip the camera horizontally
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # converts BGR image to RGB
    results = hands.process(imageRGB)  # makes the detections
    draw_hands()  # calls the function to draw on the different hand landmarks
    gestures()  # this function tracks the coordinates of the keypoints and therefore is able to recognise gestures
    cv2.imshow("Hand Tracker by Avi-Niam Popat", image)  # camera output window
    cv2.waitKey(5)