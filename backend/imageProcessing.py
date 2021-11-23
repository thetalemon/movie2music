#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


def imgProcess(path):
    img = cv2.imread(path)
    return getMostColorName(img)


def getMostColorName(img):
    COLOR_NAME = ("blue", "green", "red")

    sums = [img[:, :, ch].sum() for ch in range(img.shape[2])]
    maxIndex = sums.index(max(sums))

    return COLOR_NAME[maxIndex]


def movieProcessing():
    mov = cv2.VideoCapture("./sample3.mov")

    FRAME_COUNT = int(mov.get(cv2.CAP_PROP_FRAME_COUNT))

    fpsRangeList = list(range(0, FRAME_COUNT, 5))

    FEATURE_PARAMS = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

    LK_PARAMS = dict(
        winSize=(15, 15),
        maxLevel=2,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
    )

    color = np.random.randint(0, 255, (100, 3))

    _, old_frame = mov.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **FEATURE_PARAMS)

    mask = np.zeros_like(old_frame)
    for i, j in enumerate(fpsRangeList):
        _, frame = mov.read()

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p1, st, err = cv2.calcOpticalFlowPyrLK(
            old_gray, frame_gray, p0, None, **LK_PARAMS
        )

        if p1 is not None:
            good_new = p1[st == 1]
            good_old = p0[st == 1]

            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()

                mask = cv2.line(
                    mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2
                )
                frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)

            if len(good_new) != 0:
                old_gray = frame_gray.copy()
                p0 = good_new.reshape(-1, 1, 2)
            else:
                old_gray = frame_gray.copy()
                p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **FEATURE_PARAMS)

        img = cv2.add(frame, mask)

        cv2.imshow("frame", img)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break

        getMostColorName(frame)
        mov.set(cv2.CAP_PROP_POS_FRAMES, j)
