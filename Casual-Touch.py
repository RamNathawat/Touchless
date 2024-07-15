import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

##########################
wCam, hCam = 640, 480
frameR = 0  # Frame Reduction
smoothening = 7
clickCooldown = 0.5  # Cooldown for clicking
lastClickTime = 0
scrollSpeed = 7  # Adjust scroll speed
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()

while True:
    # 1. Capture Frame
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    # 4. Only Index Finger : Moving Mode
    if fingers[1] == 1 and all(fingers[i] == 0 for i in range(2, 5)):
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
        pyautogui.moveTo(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    # 5. Both Index and Middle Fingers Up: Clicking or Scrolling Mode
    if fingers[1] == 1 and fingers[2] == 1:
        length, img, lineInfo = detector.findDistance(8, 12, img)
        if length < 40 and (time.time() - lastClickTime) > clickCooldown:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            pyautogui.click()
            lastClickTime = time.time()
        elif length >= 40:
            scroll_amount = int((y1 - y2) / scrollSpeed)
            if abs(scroll_amount) > 0:
                pyautogui.scroll(scroll_amount)

    # 6. Four Fingers Up: Right-click Mode
    if all(fingers[i] == 1 for i in range(1, 5)):
        pyautogui.rightClick()
        time.sleep(1)

    # 7. Index Finger and Pinky Finger Extended: Swipe Left Mode
    if fingers[1] == 1 and fingers[4] == 1 and all(fingers[i] == 0 for i in range(0, 1)) and all(fingers[i] == 0 for i in range(2, 4)):
        pyautogui.hotkey('ctrl', 'left')
        time.sleep(1)

    # 8. Pinky and Thumb Extended: Swipe Right Mode
    if fingers[0] == 1 and fingers[4] == 1 and all(fingers[i] == 0 for i in range(1, 4)):
        pyautogui.hotkey('ctrl', 'right')
        time.sleep(1)

    # 9. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 10. Display the Image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
