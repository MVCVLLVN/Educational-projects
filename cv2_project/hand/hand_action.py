import cv2
import mediapipe as mp
import time


calc = [
    ["1", "2", "3", "C"],
    ["4", "5", "6", "/"],
    ["7", "8", "9", "."],
    ["-", "0", "+", "="]
]


class Button:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text
        self.size = [55, 60]


calc_button = []
for i in range(len(calc)):
    for j, key in enumerate(calc[i]):
        calc_button.append(Button([60 * j + 300, 70 * i + 10], text=key))


class MyHand:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(max_num_hands=1)
        self.draw = mp.solutions.drawing_utils
        self.text = ""

    def finds_hands(self, img):     # отрисовка ладони
        self.result = self.hands.process(img)
        if self.result.multi_hand_landmarks:
            for hand in self.result.multi_hand_landmarks:
                h, w, c = img.shape
                self.draw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)
        return img

    def finger(self, img):
        if self.result.multi_hand_landmarks:
            for hand in self.result.multi_hand_landmarks:
                h, w, c = img.shape
                print(h, w, c)
                x8, y8 = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)
                x12, y12 = int(hand.landmark[12].x * w), int(hand.landmark[12].y * h)
                cv2.circle(img, (x8, y8), 10, (0, 0, 255), cv2.FILLED)
                print("Координата указательного пальца:", x8, y8)
                print("Координата среднего пальца:", x12, y12)
                # ИЗМЕНЯЕМ ЦВЕТ ДЛЯ КНОПКИ ЕСЛИ В ЕЕ ПРОСТАРНСТВЕ НАХОДИТЬСЯ УКАЗАТЕЛЬНЫЙ ПАЛЕЦ
                for button in calc_button:
                    x, y = button.pos   # узнаем позицию кнопки из списка
                    w, h = button.size   # узнаем размер кнопки из списка
                    if x < x8 < x + w and y < y8 < y + h:
                        if button.text == "C":
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 250, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (250, 250, 250),
                                        2)
                        else:
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 250, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (250, 250, 250),
                                        2)
                        if x < x12 < x + w and y < y12 < y + h:
                            if button.text == "C":
                                self.text = ""
                                time.sleep(0.5)
                            elif button.text == "=":
                                try:
                                    self.text = str(eval(self.text))
                                    time.sleep(0.5)
                                except SyntaxError:
                                    self.text = ''
                            # elif button.text == "<":
                            #     self.text = self.text[:-1]
                            #     time.sleep(0.3)

                            else:
                                self.text += button.text
                                time.sleep(0.5)
        print(self.text)
        return img


def draw(img, calc_button, p):
    cv2.rectangle(img, (15, 15), (280, 110), (150, 0, 150), cv2.FILLED)
    cv2.putText(img, p.text, (25, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
    for button in calc_button:
        x, y = button.pos
        w, h = button.size
        if button.text == "C":
            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (250, 250, 250), 4)
        elif button.text == "5":
            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 100, 255), cv2.FILLED)
            cv2.putText(img, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (250, 0, 250), 2)
        else:
            cv2.rectangle(img, button.pos, (x + w, y + h), (200, 100, 0), cv2.FILLED)
            cv2.putText(img, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (250, 250, 250), 4)
    return img


def main():
    cap = cv2.VideoCapture(0)
    project = MyHand()
    while True:
        _, img = cap.read()
        # img = cv2.resize(img, (1200, 800))
        img = cv2.flip(img, 180)
        img = project.finds_hands(img)
        img = draw(img, calc_button, project)
        img = project.finger(img)
        cv2.imshow("Cam", img)
        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    main()