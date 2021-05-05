import numpy as np
import cv2
import time

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)

    min_ind = np.argmin(s)
    max_ind = np.argmax(s)

    rect[0] = pts[min_ind]
    rect[2] = pts[max_ind]

    inds = [_ for _ in range(4)]
    inds.remove(min_ind)
    inds.remove(max_ind)

    #print(inds)

    without = np.array ([pts[i] for i in inds])

    diff = np.diff(without, axis=1)

    #print(without)

    rect[1] = without[np.argmin(diff)]
    rect[3] = without[np.argmax(diff)]

    return rect

def get_transform(pts):
    rect = order_points(pts)

    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)

    return (M, (maxWidth, maxHeight))

def apply_transform(image, transform):
    warped = cv2.warpPerspective(image, transform[0], transform[1])

    return warped

cam = cv2.VideoCapture("/Users/elijah/Downloads/output1619983970.8765998_successful_cut.mkv")
#points = np.array([[279, 144], [569, 164], [372, 330], [45, 265]])
points = np.array([[1, 280], [280, 125], [615, 150], [390, 360]])

transform = get_transform(points)

while (True):
    ret, frame = cam.read()

    if (ret == True):
        warped = apply_transform(frame, transform)
        cv2.imshow("frame", warped)

    else:
        print("cannot read frame, exiting")
        break

    key = cv2.waitKey(100) & 0xFF

    if (key == ord('q')):
        break

cam.release()

cv2.destroyAllWindows()