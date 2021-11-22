import cv2
import numpy as np

def getMostColorName(img):
  COLOR_NAME = ('blue', 'green', 'red')

  sums = [img[:,:,ch].sum() for ch in range(img.shape[2])]
  maxIndex = sums.index(max(sums))

  # print(COLOR_NAME[maxIndex])

# mov = cv2.VideoCapture('./sample.mp4')
mov = cv2.VideoCapture('./sample3.mov')

FRAME_COUNT = int(mov.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = int(mov.get(cv2.CAP_PROP_FPS))

fpsRangeList = list(range(0, FRAME_COUNT, FPS))
movItemlist = fpsRangeList

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                      qualityLevel = 0.3,
                      minDistance = 7,
                      blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = mov.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
for i, j in enumerate(fpsRangeList):
    _, frame = mov.read()

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    if p1 is not None: 
      good_new = p1[st==1]
      good_old = p0[st==1]

      for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        
        mask = cv2.line(mask, (int(a),int(b)),(int(c),int(d)), color[i].tolist(), 2)
        frame = cv2.circle(frame,(int(a),int(b)),5,color[i].tolist(),-1)

      if len(good_new) != 0 :
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)
      else:
        old_gray = frame_gray.copy()
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    img = cv2.add(frame,mask)

    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
      break

    getMostColorName(frame)  
    mov.set(cv2.CAP_PROP_POS_FRAMES, j)
