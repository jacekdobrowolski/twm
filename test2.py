import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

#poniżej zacząłem pakować kod do metod:
#Metody działają identycznie jak rozsypany kod znajdujący się na samym dole, z jednym wyjątkiem:
#tworzenie surowego arraya punktów odfiltrowuje jedynie punkty pod wzgledem przesuniecia po osi y oraz znaku wartości (>= 0)
#(nie pomija np odstających od reszty wartości przesunięcia)

def loadFrames(path):
    frames = []
    cap = cv.VideoCapture(path)
    success, img = cap.read()
    print("loadFrames: 1")
    while success :
        frames.append(img)
        success, img = cap.read()
    return frames

def createRawDriftPoints(imageA, imageB, FeatureDetector, Matcher, max_x_diff):
    kp1, des1 = FeatureDetector.detectAndCompute(imageA,None)
    kp2, des2 = FeatureDetector.detectAndCompute(imageB,None)
    matches = Matcher.match(des1, des2)
    points = []
    max_y_diff = 5 #max y diff between matching points
    for match in matches:
        p1 = kp1[match.queryIdx].pt
        p2 = kp2[match.trainIdx].pt
        if abs(p1[1]-p2[1]) < max_y_diff:
            x_diff = (p1[0] - p2[0])
            if x_diff > 0 and x_diff < max_x_diff:
                p1_i = (int(p1[0]), int(p1[1]))
                points.append([p1_i[0], p1_i[1], x_diff])
    return np.array(points)
            

def plotPoints(points_list, shape):
    x = points_list[:,0]
    y = shape[1] - points_list[:,1]
    z = points_list[:,2]
    x_lim = shape[0]
    y_lim = shape[1]
    lim = max([x_lim, y_lim])
    print(lim)
    ax = plt.axes(projection='3d')
    ax.scatter(x, y, z, c = z, cmap='viridis', linewidth=0.5, s = 1);
    ax.set_xlim3d(0, lim)
    ax.set_ylim3d(0, lim)
    ax.set_zlim3d(6, 1)
    # Major ticks every 20, minor ticks every 5
    major_ticks = np.arange(1, 6.1, 1)
    minor_ticks = np.arange(1, 6.1, 0.2)
    ax.set_zticks(major_ticks)
    ax.set_zticks(minor_ticks, minor=True)

    # And a corresponding grid
    ax.grid(which='both')
    plt.show()



#Tu test powyższych metod

surf = cv.xfeatures2d.SURF_create(10)
sift = cv.xfeatures2d.SIFT_create()

bf = cv.BFMatcher()

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv.FlannBasedMatcher(index_params,search_params)

focal_lenght = 35
frames = loadFrames("data/focal_35_linear.avi")
first_f = 1
last_f = 30
step = 7
max_drift_factor = 15
result = []
print(len(frames))


for i in range(step, last_f, step):
    max_dx = i * max_drift_factor
    p = createRawDriftPoints(frames[first_f], frames[i], surf, flann, max_dx)
    print(p.shape)
    print(p[0])
    p[:,2] /= (i-first_f)
    print(p[0])
    p[:,2] = focal_lenght / p[:,2]
    result.extend(p)
result = np.array(result)
plotPoints(result, (1920, 1080))

fig = plt.figure()
ax = fig.gca()
plt.scatter(result[:,0], result[:, 2], s=1)
ax.set_ylim(6, 1)
# Major ticks every 20, minor ticks every 5
major_ticks = np.arange(1, 6.1, 1)
minor_ticks = np.arange(1, 6.1, 0.2)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)
ax.grid()

plt.show()
