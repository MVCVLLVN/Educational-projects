import cv2
import mediapipe as mp
import time


class MyHand:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(max_num_hands=1)
        self.draw = mp.solutions.drawing_utils
        self.text = ""

    # def finds_hands(self, img):
    #     self.result = self.hands.process(img)
    #     if self.result.multi_hand_landmarks:
    #         for hand in self.result.multi_hand_landmarks:
    #             h, w, c = img.shape
    #             self.draw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)
    #     return img

    def finger(self, img):
        self.result = self.hands.process(img)
        if self.result.multi_hand_landmarks:
            for hand in self.result.multi_hand_landmarks:
                h, w, c = img.shape
                x8, y8 = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)
                x4, y4 = int(hand.landmark[4].x * w), int(hand.landmark[4].y * h)
                print(abs(x4 - x8), abs(y4 - y8))
                if abs(x4 - x8) < 30 and abs(y4 - y8) < 30:
                    self.text = "Hi friends"
                else:
                    self.text = ""
        return img


def draw(img, obj):
    cv2.rectangle(img, (15, 15), (400, 100), (150, 0, 150), cv2.FILLED)
    cv2.putText(img, obj.text, (15, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
    return img


def main():
    cap = cv2.VideoCapture(0)
    obj = MyHand()
    while True:
        _, img = cap.read()
        # img = obj.finds_hands(img)
        img = obj.finger(img)
        img = draw(img, obj)
        cv2.imshow("Cam", img)
        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    main()
