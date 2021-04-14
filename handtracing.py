import mediapipe as mp
import cv2
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
prev_time = 0

cap = cv2.VideoCapture(0)

# cap.set(3, 1920)
# cap.set(4, 1080)
rate = 5

def FPS():
    global prev_time
    current_time = time.time()
    fps = 1/(current_time - prev_time)
    prev_time = current_time
    return fps

X1 = 1
Y1 = 1

with mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5, max_num_hands=1) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    # print(results.multi_hand_landmarks)

    #image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks == None:
      X1 = 1
      Y1 = 1
    

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        for id, landm in enumerate(hand_landmarks.landmark):
          h, w, _ = image.shape
          X2, Y2 = int(landm.x * w), int(landm.y * h)
          if hand_landmarks !=0:
            if id == 8 :
              if((X2 - X1) > (Y2 - Y1) and (X2 - X1) >= rate and X1 != 1 and Y1 != 1):
                  cv2.putText(image, 'Right', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                  X1 = X2
                  Y1 = Y2
              elif(abs(X2 - X1) > abs(Y2 - Y1) and (X1 - X2) >= rate and X1 != 1 and Y1 != 1):
                  cv2.putText(image, 'Left', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                  X1 = X2
                  Y1 = Y2
              elif((X2 - X1) < (Y2 - Y1) and (Y2 - Y1) >= rate and X1 != 1 and Y1 != 1):
                  cv2.putText(image, 'Down', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                  X1 = X2
                  Y1 = Y2
              elif(abs(X2 - X1) < abs(Y2 - Y1) and (Y1 - Y2) >= rate and X1 != 1 and Y1 != 1):
                  cv2.putText(image, 'Up', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                  X1 = X2
                  Y1 = Y2
              else:
                  X1 = X2
                  Y1 = Y2

              
    # print(X1)

    fps = FPS()
    cv2.putText(image, 'FPS = ' + str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()