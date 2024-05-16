from imutils.perspective import four_point_transform, order_points
from imutils import contours
import imutils
import cv2
import numpy as np

def draw_points(cnt, img, color):
    for p in cnt:
        p = tuple(p.astype(int))
        cv2.circle(img, p, 3, color, -1)
        
def sort_contours_bound_rect(cnts, reverse=False):
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][2] * b[1][3], reverse=reverse))
    return cnts, boundingBoxes

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 0, 1): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 1, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}

largest_area = 1
skewness_area = 1

image = cv2.imread('./data/1.png')
   
image = imutils.resize(image, height=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)

cv2.imshow("Video", image)
cv2.imshow("Blurred", blurred)
cv2.imshow("Edged", edged)
    
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts, rcts = sort_contours_bound_rect(cnts, reverse=True)
displayCnt = None
    
for i, c in enumerate(cnts):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if i == largest_area:
        rect = cv2.minAreaRect(approx)
        box = cv2.boxPoints(rect)
        box = np.array(box, dtype="int")
        box = order_points(box)
        displayCnt = box
        break

if displayCnt is not None:
    warped = four_point_transform(gray, displayCnt.reshape(4, 2))
    output = four_point_transform(image, displayCnt.reshape(4, 2))
    edged = four_point_transform(edged, displayCnt.reshape(4, 2))
    print(f"display cnt: {displayCnt}")
    draw_points(displayCnt, image, (0, 255, 0))

    cv2.imshow("Warped", warped)
    
    height, width = warped.shape
    width -= 1
    height -= 1

    rect = np.array([
        [0, 0],
        [width, 0],
        [width, height],
        [0, height]
    ], dtype="float32")

    dst = np.array([
        [skewness_area, 0],
        [width - skewness_area, 0],
        [width, height],
        [0, height]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(warped, M, (width+1, height+1))
    output = cv2.warpPerspective(output, M, (width+1, height+1))
    
    height, width = warped.shape
    width -= 1
    height -= 1

    skewness_area += 2
    warped = warped[skewness_area:height, skewness_area:width - skewness_area]
    output = output[skewness_area:height, skewness_area:width - skewness_area]

    thresh = cv2.threshold(warped, 150, 255,
                        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    height, width = thresh.shape

    vert_dilate3 = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(1, 3))
    thresh = cv2.dilate(thresh, vert_dilate3)
    thresh = cv2.erode(thresh, vert_dilate3)
    
    cv2.imshow("Threshold", thresh)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)
    digitCnts = []

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        print(f"cnt height: {h}")
        if 100 <= h <= 230:
            digitCnts.append(c)
    if len(digitCnts) > 0:
        digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
        
    digits = []

    horz_dilate2 = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(2, 1))
    vert_dilate2 = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(1, 2))

    for c in digitCnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w < 10:
            x -= 13 - w
            w = 13
        roi = thresh[y:y + h, x:x + w]

        (roiH, roiW) = roi.shape
        (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
        dHC = int(roiH * 0.05)

        segments = [
            ((2, 0), (w - 2, dH)),  # top
            ((0, 0), (dW, h // 2)),  # top-left
            ((w - dW, 0), (w, h // 2)),  # top-right
            ((5, (h // 2) - dHC), (w - 5, (h // 2) + dHC)),  # center
            ((0, h // 2), (dW, h)),  # bottom-left
            ((w - dW, h // 2), (w, h)),  # bottom-right
            ((2, h - dH), (w - 2, h))  # bottom
        ]
        on = [0] * len(segments)

        for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
            segROI = roi[yA:yB, xA:xB]
            if i in [1, 2, 4, 5]:
                segROI = cv2.dilate(segROI, horz_dilate2)
            else:
                segROI = cv2.dilate(segROI, vert_dilate2)
            total = cv2.countNonZero(segROI)
            area = (xB - xA) * (yB - yA)

            if total / float(area) > 0.5:
                on[i] = 1

        if tuple(on) in DIGITS_LOOKUP.keys():
            digit = DIGITS_LOOKUP[tuple(on)]
        else:
            digit = -1
            print(on)
            cv2.imshow("ROI", roi)
        digits.append(digit)
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.putText(output, str(digit), (x + 1, y + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 1)

    print(digits)
    cv2.imshow("Input", image)
    cv2.imshow("Output", output)
cv2.waitKey(0)