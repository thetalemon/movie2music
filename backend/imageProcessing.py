#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import cv2
import numpy as np
from makeMusic import create_music


def imgProcess(path):
    img = cv2.imread(path)
    # create_music(path)
    return getHsvColor(img)


def getHsvColor(img):
    hsvImg = list(range(len(img)))
    for i, j in enumerate(img):
        hsvRow = list(range(len(j)))
        for k, l in enumerate(j):
            maxIndex = np.argmax(l)
            MAX = int(max(l))
            MIN = int(min(l))
            BLUE = int(l[0])
            GREEN = int(l[1])
            RED = int(l[2])
            if BLUE == GREEN and GREEN == RED and BLUE == RED:
                h = 0
            elif maxIndex == 0:
                h = 60 * ((RED - GREEN) / (MAX - MIN)) + 240
                if h < 0:
                    h = h + 360
            elif maxIndex == 1:
                h = 60 * ((BLUE - RED) / (MAX - MIN)) + 120
            elif maxIndex == 2:
                h = 60 * ((GREEN - BLUE) / (MAX - MIN))

            if h < 0:
                h = h + 360

            s = (MAX - MIN) / MAX
            v = MAX
            hsvRow[k] = [h, s, v]
        hsvImg[i] = hsvRow
    return hsvImg


def isCenterArea(width, height, x, y):
    xCenterFlg = width * 0.25 < x and width * 0.75 > x
    yCenterFlg = height * 0.25 < y and height * 0.75 > y
    return xCenterFlg and yCenterFlg


def drawFeatures(mask, frame, a, b, c, d, color, k):
    mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[k].tolist(), 2)
    frame = cv2.circle(frame, (int(a), int(b)), 5, color[k].tolist(), -1)


def updatePrevFrameData(good_new, frame_gray, old_gray, FEATURE_PARAMS):
    if len(good_new) != 0:
        return frame_gray.copy(), good_new.reshape(-1, 1, 2)
    else:
        return frame_gray.copy(), cv2.goodFeaturesToTrack(
            old_gray, mask=None, **FEATURE_PARAMS
        )


def movieProcessing():
    path = "./sampleFiles/sample3.mov"
    mov = cv2.VideoCapture(path)

    FRAME_COUNT = int(mov.get(cv2.CAP_PROP_FRAME_COUNT))

    if mov.get(cv2.CAP_PROP_FPS) == 0:
        return

    # 1秒を4分割
    FPS_RANGE_LIST = np.arange(0.0, FRAME_COUNT, mov.get(cv2.CAP_PROP_FPS) / 4)

    FEATURE_PARAMS = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

    LK_PARAMS = dict(
        winSize=(15, 15),
        maxLevel=2,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
    )

    # color = np.random.randint(0, 255, (100, 3))

    _, old_frame = mov.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **FEATURE_PARAMS)

    # mask = np.zeros_like(old_frame)
    allVectors = list(range(len(FPS_RANGE_LIST)))
    allUpFlg = list(range(len(FPS_RANGE_LIST)))
    allCenterFlg = list(range(len(FPS_RANGE_LIST)))
    for i, j in enumerate(FPS_RANGE_LIST):
        _, frame = mov.read()

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p1, st, err = cv2.calcOpticalFlowPyrLK(
            old_gray, frame_gray, p0, None, **LK_PARAMS
        )
        WIDTH = mov.get(cv2.CAP_PROP_FRAME_WIDTH)
        HEIGHT = mov.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if p1 is not None:
            good_new = p1[st == 1]
            good_old = p0[st == 1]
            vectors = list(range(len(good_new)))
            upFlg = list(range(len(good_new)))
            centerFlg = list(range(len(good_new)))

            for k, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()

                # 描画
                # drawFeatures(mask, frame, a, b, c, d, color, k)

                vectors[k] = abs((c - a) ** 2 + (d - b) ** 2)
                upFlg[k] = (c - a) > 0
                centerFlg[k] = isCenterArea(WIDTH, HEIGHT, c, d)

            old_gray, p0 = updatePrevFrameData(
                good_new, frame_gray, old_gray, FEATURE_PARAMS
            )

            allVectors[i] = vectors
            allUpFlg[i] = upFlg
            allCenterFlg[i] = centerFlg

        # 特徴点画像表示
        # img = cv2.add(frame, mask)
        # cv2.imshow("frame", img)
        # k = cv2.waitKey(30) & 0xFF
        # if k == 27:
        #     break

        getHsvColor(frame)
        mov.set(cv2.CAP_PROP_POS_FRAMES, j)

    print(
        {
            "second": (FRAME_COUNT / mov.get(cv2.CAP_PROP_FPS)),
            "vectors": allVectors,
            "upFlg": allUpFlg,
            "centerFlg": allCenterFlg,
        }
    )
    print(mov.get(cv2.CAP_PROP_FRAME_COUNT))
    print(int(mov.get(cv2.CAP_PROP_FPS) + 1))
    print(int(mov.get(cv2.CAP_PROP_FPS) + 1) / 5)

    create_music(
        path,
        {
            "second": (FRAME_COUNT / mov.get(cv2.CAP_PROP_FPS)),
            "vectors": allVectors,
            "upFlg": allUpFlg,
            "centerFlg": allCenterFlg,
        },
    )


imgProcess(
    "/Users/sasakimanami/Documents/Github/movie2music/backend/sampleFiles/sample.png"
)
# movieProcessing()
