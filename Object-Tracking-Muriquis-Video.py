import cv2
import numpy as np
import imutils
from collections import deque

class ObjectTracker:
    def __init__(self, initial_position):
        self.positions = deque(maxlen=trackingBufferSize)
        self.positions.append(initial_position)
        self.counted = False

def callback(value):
    pass

def setup_trackbars():
    cv2.namedWindow("Trackbars", 0)
    init_values = {"H_MIN": 0, "S_MIN": 0, "V_MIN": 145, "H_MAX": 220, "S_MAX": 50, "V_MAX": 255}
    for i in ["MIN", "MAX"]:
        for j in "HSV":
            cv2.createTrackbar(f"{j}_{i}", "Trackbars", init_values[f"{j}_{i}"], 255, callback)

def get_trackbar_values():
    values = {}
    for i in ["MIN", "MAX"]:
        for j in "HSV":
            values[f"{j}_{i}"] = cv2.getTrackbarPos(f"{j}_{i}", "Trackbars")
    return values

def is_new_object(existing_trackers, new_center, min_dist=50):
    for tracker in existing_trackers:
        if np.linalg.norm(np.array(tracker.positions[0]) - np.array(new_center)) < min_dist:
            return False
    return True

setup_trackbars()
cap = cv2.VideoCapture('Muriquis.mp4')

trackingBufferSize = 64
object_trackers = []
object_count = 0

while True:
    grabbed, frame = cap.read()
    if not grabbed:
        break

    trackbar_values = get_trackbar_values()
    hueLower, saturationLower, valueLower = trackbar_values["H_MIN"], trackbar_values["S_MIN"], trackbar_values["V_MIN"]
    hueUpper, saturationUpper, valueUpper = trackbar_values["H_MAX"], trackbar_values["S_MAX"], trackbar_values["V_MAX"]

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (hueLower, saturationLower, valueLower), (hueUpper, saturationUpper, valueUpper))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < 100:
            continue

        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))

        if radius > 10:
            cv2.circle(frame, center, int(radius), (0, 255, 255), 2)

            if is_new_object(object_trackers, center):
                object_trackers.append(ObjectTracker(center))
                object_count += 1
                print(f"Novo objeto branco detectado: {object_count}")
            else:
                for tracker in object_trackers:
                    if np.linalg.norm(np.array(tracker.positions[0]) - np.array(center)) < 50:
                        tracker.positions.appendleft(center)
                        break

    for tracker in object_trackers:
        for i in range(1, len(tracker.positions)):
            if tracker.positions[i - 1] is None or tracker.positions[i] is None:
                continue
            cv2.line(frame, tracker.positions[i - 1], tracker.positions[i], (255, 255, 255), 2)

    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
