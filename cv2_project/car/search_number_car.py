import cv2
from easyocr import Reader

image = cv2.imread("car_1.jpg")
image = cv2.resize(image, (800, 600))
#
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Машина", gray)
cv2.waitKey(0)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
cv2.imshow("Машина", blur)
cv2.waitKey(0)
edged = cv2.Canny(blur, 50, 300)
cv2.imshow("Машина", edged)
cv2.waitKey(0)

contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
# print(contours)

for c in contours:
    piri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * piri, True)
    if len(approx) == 4:
        plate_count = approx
        break

(x, y, w, h) = cv2.boundingRect(plate_count)
licence_plate = gray[y:y + h, x:x + w]
reader = Reader(["en"])
detection = reader.readtext(licence_plate)
print(detection)
if len(detection) == 0:
    text = "Номер не распознан"
    cv2.putText(image, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 3)
    cv2.imshow("Машина", edged)
    cv2.waitKey(0)
else:
    cv2.drawContours(image, [plate_count], -1, (0, 255, 0), 2)
    text = f"{detection[0][1]} {detection[0][2] * 100:.2f}%"
    cv2.putText(image, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    cv2.imshow("срез", licence_plate)
    cv2.imshow("Машина", image)
    cv2.waitKey(0)


image = cv2.imread("car_1.jpg")
image = cv2.resize(image, (800, 600))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(blur, 50, 300)
# cv2.imshow("Машина", edged)
cv2.imshow("Машина", edged)
cv2.waitKey(0)
# #
contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
# print(contours)
#
for c in contours:
    piri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * piri, True)
    if len(approx) == 4:
        plate_count = approx
        break
(x, y, w, h) = cv2.boundingRect(plate_count)
licence_plate = gray[y:y + h, x:x + w]
reader = Reader(["en"])
detection = reader.readtext(licence_plate)
print(detection)