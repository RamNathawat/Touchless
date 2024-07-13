import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
clickCooldown = 0.5  # Cooldown for clicking
lastClickTime = 0
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
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip

    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    # 4. Only Index Finger : Moving Mode
    if fingers[1] == 1 and all(fingers[i] == 0 for i in range(2, 5)):
        # 5. Convert Coordinates
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        # 7. Move Mouse
        pyautogui.moveTo(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    # 8. Both Index and Middle Fingers Up: Clicking or Scrolling Mode
    if fingers[1] == 1 and fingers[2] == 1:
        # 9. Find distance between fingers
        length, img, lineInfo = detector.findDistance(8, 12, img)

        # 10. Click mouse if distance short and cooldown has passed
        if length < 40 and (time.time() - lastClickTime) > clickCooldown:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            pyautogui.click()
            lastClickTime = time.time()  # Update last click time
        # If distance is greater, treat as scrolling
        elif length >= 40:
            scroll_amount = int((y1 - y2) / 10)  # Adjust sensitivity here
            if abs(scroll_amount) > 0:  # Only scroll if there is a significant movement
                pyautogui.scroll(scroll_amount)

    # 12. Four Fingers Up: Right-click Mode
    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
        pyautogui.rightClick()
        time.sleep(1)  # Adding a small delay to avoid multiple right-clicks

    # 13. Thumb Left: Swipe Left Mode
    if fingers[0] == 1 and all(fingers[i] == 0 for i in range(1, 5)):
        # Check thumb position (x-coordinate) against the index finger
        if x1 < x2:  # If the thumb (x0) is to the left of the index finger (x1)
            pyautogui.hotkey('ctrl', 'left')  # Perform a left swipe
            time.sleep(1)  # Adding a small delay to avoid multiple swipes

    # 14. Pinky Up: Swipe Right Mode
    if all(fingers[i] == 0 for i in range(0, 4)) and fingers[4] == 1:
        pyautogui.hotkey('ctrl', 'right')
        time.sleep(1)  # Adding a small delay to avoid multiple swipes

    # 15. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 16. Display the Image
    cv2.imshow("Image", img)
    cv2.waitKey(1)
