import cv2


# помещаем изображение
img = cv2.imread("img.png")
img = cv2.resize(img, (700, 500))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Photo', gray)
# cv2.waitKey(0)
faces = cv2.CascadeClassifier("mod_1.xml")

# содержит координаты лиц
# scaleFactor - адаптируем под наше изображение, так как учили модель на маленьких
# minNeighbors - как много объектов рядом с искомым
results = faces.detectMultiScale(gray, scaleFactor=2, minNeighbors=1)
print(results)
for (x, y, w, h) in results:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 250, 0), thickness=2)

cv2.imshow('Photo', img)
cv2.waitKey(0)

