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

def createRawDriftPoints(imageA, imageB, FeatureDetector, Matcher):
    kp1, des1 = FeatureDetector.detectAndCompute(imageA,None)
    kp2, des2 = FeatureDetector.detectAndCompute(imageB,None)
    matches = Matcher.match(des1, des2)
    print(len(matches))
    points = []
    max_y_diff = 5 #max y diff between matching points
    for match in matches:
        p1 = kp1[match.queryIdx].pt
        p2 = kp2[match.trainIdx].pt
        if abs(p1[1]-p2[1]) < max_y_diff:
            x_diff = (p1[0] - p2[0])
            if x_diff > 0:
                p1_i = (int(p1[0]), int(p1[1]))
                points.append([p1_i[0], p1_i[1], x_diff])
    print(len(points))
    return np.array(points)
            
def createDepthMap(points, shape, square_size):
    map = np.ones(shape) * -1
    for p in points:
        x = int(p[0])
        y = int(p[1])
        map[x, y] = p[2]
    x_idx = range(square_size, shape[0] - 1, square_size)
    y_idx = range(square_size, shape[1] - 1, square_size)

    x1 = 0
    y1 = 0
    #for y1 in y_idx:

    #todo sliding window



def filterWithinRectangle(array):
    return np.mean(array)


def plotPoints(points_list):
    x = points_list[:,0]
    y = points_list[:,1]
    z = points_list[:,2]
    print(points_list)
    print(x)
    x_lim = max(x)
    y_lim = max(y)
    ax = plt.axes(projection='3d')
    ax.scatter(x, y, z, cmap='viridis', linewidth=0.5);
    ax.set_xlim3d(0, x_lim)
    ax.set_ylim3d(0, y_lim)
    plt.show()


#Tu test powyższych metod

#print("testing")
#surf = cv.xfeatures2d.SURF_create(5)
#bf = cv.BFMatcher()
#frames = loadFrames("data/small_grain.avi")
#points = createRawDriftPoints(frames[0], frames[-1], surf, bf)
#plotPoints(points)






#
#
# Poniżej "działający" kod, jest nieuporzadkowany więc wymaga upakowania w metody
#
#
#
#
#
#

surf = cv.xfeatures2d.SURF_create(5)
sift = cv.xfeatures2d.SIFT_create()
bf = cv.BFMatcher()

cap = cv.VideoCapture("data/small_grain.avi")
success, img1 = cap.read()
success, img2 = cap.read()
print(img2.shape)

result = img1.copy()
fno = 1
sample_rate = 16

kp1, des1 = surf.detectAndCompute(img1,None)

x = []
y = []
z = []

while success :
    if fno % sample_rate == 0:
        kp2, des2 = surf.detectAndCompute(img2,None)
        matches = bf.match(des1,des2)
        #result = img1.copy()
        for match in matches:
            p1 = kp1[match.queryIdx].pt
            p2 = kp2[match.trainIdx].pt
            if abs(p1[1]-p2[1]) < 5:
                x_diff = (p1[0] - p2[0]) / fno
                p1 = (int(p1[0]), int(p1[1]))
                p2 = (int(p2[0]), int(p2[1]))
                #cv.line(result, p1, p2, (0,0,0), 1)
                if x_diff < 15 and x_diff > 3:
                    x.append(p1[0])
                    y.append(p1[1])
                    z.append(x_diff)
        #plt.imshow(result),plt.show()
    success, img2 = cap.read()
    fno += 1
print(fno)
print(len(z))
ax = plt.axes(projection='3d')
ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5);
ax.set_xlim3d(0, 2000)
ax.set_ylim3d(0, 2000)
plt.show()
 

