
# %%
from itertools import repeat
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = [8, 8]

# %%
cap = cv.VideoCapture("data/small_grain.avi")

# %%
ret, first_frame = cap.read()
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
mask = np.zeros_like(first_frame)
mask[..., 1] = 255
plt.imshow(prev_gray, cmap='gray')
cv.imwrite("first_frame.png", first_frame)
# %%
cap = cv.VideoCapture("data/small_grain.avi")
def dense_flow(frames: int):
    #cap = cv.VideoCapture("data/0001-0010.avi")
    print(int(cap.get(cv.CAP_PROP_FRAME_COUNT)))
    ret, first_frame = cap.read()
    prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
    flow = None
    for _ in range(frames):
        ret, frame = cap.read()
        cv.imwrite("last_frame.png", frame)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(
            prev=prev_gray,
            next=gray, 
            flow=flow,
            pyr_scale=0.5,
            levels=5,
            winsize=5,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )
        prev_gray = gray

    magnitude, angle = cv.cartToPolar(flow[..., 0], flow[..., 1])
    mask[..., 0] = angle * 180 / np.pi / 2
    mask[..., 2] = cv.normalize(magnitude, None, 0, 255, cv.NORM_MINMAX)
    rgb = cv.cvtColor(mask, cv.COLOR_HSV2BGR)
    # return rgb
    return magnitude

def roundData(X, Y, Z):
    shape = X.shape


# %%
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d(0, 2000)
ax.set_ylim3d(0, 2000)
ax.set_zlim3d(0, 5)
flow = dense_flow(29)
ys, xs = flow.shape
Y, X = np.mgrid[0:ys, 0:xs]
print("flow:", flow.shape,"Y: ", Y.shape, "X: ",X.shape)
ax.plot_surface(X, Y, flow, cmap='plasma')
plt.show()

