import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

# Configuration Parameters
wCam, hCam = 640, 480
frameR = 100  # Reduced the active region size to prevent false positives
smoothening = 4
clickCooldown = 1.0  # Increased cooldown period
clickHoldTime = 0.5  # Time to hold fingers for click
gestureHoldTime = 0.8  # Time to hold gesture before it's recognized
scrollSpeed = 10

# Initialize Variables
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
lastClickTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()

gestureStates = {
    "move": {"startTime": 0, "active": False},
    "click": {"startTime": 0, "active": False},
    "scroll": {"startTime": 0, "active": False},
    "rightClick": {"startTime": 0, "active": False},
    "swipeLeft": {"startTime": 0, "active": False},
    "swipeRight": {"startTime": 0, "active": False},
}


def updateGestureState(gestureName, condition):
    currentTime = time.time()
    if condition:
        if not gestureStates[gestureName]["active"]:
            gestureStates[gestureName]["startTime"] = currentTime
            gestureStates[gestureName]["active"] = True
        elif currentTime - gestureStates[gestureName]["startTime"] >= gestureHoldTime:
            gestureStates[gestureName]["startTime"] = currentTime
            return True
    else:
        gestureStates[gestureName]["active"] = False
    return False


def processGesture(fingers, x1, y1, x2, y2, img):
    global plocX, plocY, clocX, clocY, lastClickTime

    # Move cursor
    if updateGestureState("move", fingers[1] == 1 and all(fingers[i] == 0 for i in range(2, 5))):
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        pyautogui.moveTo(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    # Click
    if fingers[1] == 1 and fingers[2] == 1:
        length, img, lineInfo = detector.findDistance(8, 12, img)
        if length < 30 and (time.time() - lastClickTime) > clickCooldown:
            currentTime = time.time()
            if currentTime - gestureStates["click"]["startTime"] >= clickHoldTime:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
                lastClickTime = time.time()
        elif length >= 40:
            scroll_amount = int((y1 - y2) / scrollSpeed)
            if abs(scroll_amount) > 0:
                pyautogui.scroll(scroll_amount)

    # Right Click
    if updateGestureState("rightClick", all(fingers[i] == 1 for i in range(1, 5))):
        pyautogui.rightClick()
        time.sleep(1)

    # Swipe Left (Ctrl + Left Arrow)
    if updateGestureState("swipeLeft",
                          fingers[1] == 1 and fingers[4] == 1 and all(fingers[i] == 0 for i in range(0, 1)) and all(
                                  fingers[i] == 0 for i in range(2, 4))):
        pyautogui.hotkey('ctrl', 'left')
        time.sleep(1)

    # Swipe Right (Ctrl + Right Arrow)
    if updateGestureState("swipeRight",
                          fingers[0] == 1 and fingers[4] == 1 and all(fingers[i] == 0 for i in range(1, 4))):
        pyautogui.hotkey('ctrl', 'right')
        time.sleep(1)


while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Process gestures
        processGesture(fingers, x1, y1, x2, y2, img)

    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
