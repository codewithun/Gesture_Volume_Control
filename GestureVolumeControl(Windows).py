# ==========================================================
# HAND GESTURE VOLUME CONTROL
# Menggunakan OpenCV + MediaPipe
# ==========================================================

import cv2
import mediapipe as mp
import time
import math
import numpy as np

# ==========================
# WINDOWS ONLY (Pycaw)
# ==========================
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# ==========================================================
# HAND DETECTOR CLASS
# ==========================================================
class HandDetector:
    """
    Class untuk mendeteksi tangan dan landmark jari
    menggunakan MediaPipe Hands.
    """

    def __init__(
        self,
        mode=False,
        maxHands=1,
        detectionCon=0.7,
        trackCon=0.5
    ):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Inisialisasi MediaPipe
        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        # Utility drawing
        self.mpDraw = mp.solutions.drawing_utils

        # Landmark ujung jari
        self.tipIds = [4, 8, 12, 16, 20]

    # ======================================================
    # Deteksi tangan
    # ======================================================
    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:

            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(
                        img,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS
                    )

        return img

    # ======================================================
    # Ambil posisi landmark
    # ======================================================
    def findPosition(self, img, handNo=0, draw=True):

        xList = []
        yList = []
        bbox = []

        self.lmList = []

        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):

                h, w, c = img.shape

                cx, cy = int(lm.x * w), int(lm.y * h)

                xList.append(cx)
                yList.append(cy)

                self.lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(
                        img,
                        (cx, cy),
                        5,
                        (255, 0, 255),
                        cv2.FILLED
                    )

            # Bounding box tangan
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)

            bbox = (xmin, ymin, xmax, ymax)

            if draw:
                cv2.rectangle(
                    img,
                    (bbox[0] - 20, bbox[1] - 20),
                    (bbox[2] + 20, bbox[3] + 20),
                    (0, 255, 0),
                    2
                )

        return self.lmList, bbox

    # ======================================================
    # Mengecek jari yang terbuka
    # ======================================================
    def fingersUp(self):

        fingers = []

        # Thumb
        if (
            self.lmList[self.tipIds[0]][1]
            > self.lmList[self.tipIds[0] - 1][1]
        ):
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 jari lainnya
        for id in range(1, 5):

            if (
                self.lmList[self.tipIds[id]][2]
                < self.lmList[self.tipIds[id] - 2][2]
            ):
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    # ======================================================
    # Menghitung jarak antar landmark
    # ======================================================
    def findDistance(self, p1, p2, img, draw=True):

        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:

            cv2.circle(
                img,
                (x1, y1),
                15,
                (255, 0, 255),
                cv2.FILLED
            )

            cv2.circle(
                img,
                (x2, y2),
                15,
                (255, 0, 255),
                cv2.FILLED
            )

            cv2.line(
                img,
                (x1, y1),
                (x2, y2),
                (255, 0, 255),
                3
            )

            cv2.circle(
                img,
                (cx, cy),
                15,
                (255, 0, 255),
                cv2.FILLED
            )

        # Hitung jarak Euclidean
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


# ==========================================================
# MAIN PROGRAM
# ==========================================================
def main():

    # ==========================
    # Webcam Size
    # ==========================
    wCam, hCam = 640, 480

    # ==========================
    # Open Webcam
    # ==========================
    cap = cv2.VideoCapture(0)

    cap.set(3, wCam)
    cap.set(4, hCam)

    # ==========================
    # FPS Variable
    # ==========================
    pTime = 0

    # ==========================
    # Hand Detector
    # ==========================
    detector = HandDetector(
        detectionCon=0.7,
        maxHands=1
    )

    # ======================================================
    # Volume Control Setup (Windows)
    # ======================================================
    devices = AudioUtilities.GetSpeakers()

    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Ambil range volume
    volRange = volume.GetVolumeRange()

    minVol = volRange[0]
    maxVol = volRange[1]

    # ==========================
    # Volume Variables
    # ==========================
    vol = 0
    volBar = 400
    volPer = 0

    # Warna indikator
    colorVol = (255, 0, 0)

    # ======================================================
    # LOOP PROGRAM
    # ======================================================
    while True:

        success, img = cap.read()

        if not success:
            print("Kamera gagal dibuka")
            break

        # ==================================================
        # DETEKSI TANGAN
        # ==================================================
        img = detector.findHands(img)

        lmList, bbox = detector.findPosition(img, draw=True)

        # Jika landmark ditemukan
        if len(lmList) != 0:

            # ==============================================
            # Hitung area tangan
            # Untuk filter jarak kamera
            # ==============================================
            area = (
                (bbox[2] - bbox[0]) *
                (bbox[3] - bbox[1])
            ) // 100

            # Filter ukuran tangan
            if 250 < area < 1000:

                # ==========================================
                # Hitung jarak ibu jari & telunjuk
                # ==========================================
                length, img, lineInfo = detector.findDistance(
                    4,
                    8,
                    img
                )

                # ==========================================
                # Konversi jarak -> volume
                # ==========================================
                vol = np.interp(
                    length,
                    [50, 200],
                    [minVol, maxVol]
                )

                volBar = np.interp(
                    length,
                    [50, 200],
                    [400, 150]
                )

                volPer = np.interp(
                    length,
                    [50, 200],
                    [0, 100]
                )

                # ==========================================
                # Smooth Volume
                # ==========================================
                smoothness = 10

                volPer = smoothness * round(
                    volPer / smoothness
                )

                # ==========================================
                # Cek jari
                # ==========================================
                fingers = detector.fingersUp()

                # ==========================================
                # Jika pinky turun -> volume aktif
                # ==========================================
                if not fingers[4]:

                    # Set volume
                    volume.SetMasterVolumeLevelScalar(
                        volPer / 100,
                        None
                    )

                    # Lingkaran hijau
                    cv2.circle(
                        img,
                        (lineInfo[4], lineInfo[5]),
                        15,
                        (0, 255, 0),
                        cv2.FILLED
                    )

                    colorVol = (0, 255, 0)

                else:
                    colorVol = (255, 0, 0)

        # ==================================================
        # DRAW VOLUME BAR
        # ==================================================
        cv2.rectangle(
            img,
            (50, 150),
            (85, 400),
            (255, 0, 0),
            3
        )

        cv2.rectangle(
            img,
            (50, int(volBar)),
            (85, 400),
            (255, 0, 0),
            cv2.FILLED
        )

        # Persentase volume
        cv2.putText(
            img,
            f'{int(volPer)} %',
            (40, 450),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 0, 0),
            3
        )

        # Volume saat ini
        cVol = int(
            volume.GetMasterVolumeLevelScalar() * 100
        )

        cv2.putText(
            img,
            f'Volume: {cVol}',
            (350, 50),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            colorVol,
            3
        )

        # ==================================================
        # HITUNG FPS
        # ==================================================
        cTime = time.time()

        fps = 1 / (cTime - pTime)

        pTime = cTime

        cv2.putText(
            img,
            f'FPS: {int(fps)}',
            (40, 100),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 0, 0),
            3
        )

        # ==================================================
        # TAMPILKAN WINDOW
        # ==================================================
        cv2.imshow("Hand Gesture Volume Control", img)

        # Tekan Q untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ======================================================
    # RELEASE
    # ======================================================
    cap.release()

    cv2.destroyAllWindows()


# ==========================================================
# RUN PROGRAM
# ==========================================================
if __name__ == "__main__":
    main()