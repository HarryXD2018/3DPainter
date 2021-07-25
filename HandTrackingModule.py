import cv2
import mediapipe as mp
import time
import math

class handDetctor():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True, ):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#转换为rgb
        self.results = self.hands.process(imgRGB)

        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                # 获取手指关节点
                h, w, c = img.shape
                cx, cy, cz = int(lm.x*w), int(lm.y*h), int(lm.z*w)
                lmList.append([id, cx, cy, cz])
                if draw:
                    cv2.putText(img, str(int(id)), (cx+10, cy+10), cv2.FONT_HERSHEY_PLAIN,
                                1, (0, 0, 255), 2)

        return lmList

    # 返回列表 包含每个手指的开合状态
    def fingerStatus(self, lmList):
        fingerList = []
        id, originx, originy, originz = lmList[0]
        keypoint_list = [[2, 4], [6, 8], [10, 12], [14, 16], [18, 20]]
        for point in keypoint_list:
            id, x1, y1, z1 = lmList[point[0]]
            id, x2, y2, z2 = lmList[point[1]]
            if math.hypot(x2-originx, y2-originy) > math.hypot(x1-originx, y1-originy):
                fingerList.append(True)
            else:
                fingerList.append(False)

        return fingerList

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # 帧率统计
    pTime = 0
    cTime = 0
    detector = handDetctor()
    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            # print(lmList)
            print(detector.fingerStatus(lmList))

        # 统计屏幕帧率
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("image", img)
        if cv2.waitKey(2) & 0xFF == 27:
            break

    cap.release()


if __name__ == '__main__':
    main()
