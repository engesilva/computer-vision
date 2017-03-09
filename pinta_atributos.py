#! /usr/bin/env python3

import cv2
import argparse

LEFT_EYE = range(36, 42)
RIGHT_EYE = range(42, 48)
NOSE = range(27, 36)
MOUTH = range(48, 68)
FACE = range(17, 68)
ELEMENTS = [LEFT_EYE, RIGHT_EYE, NOSE, MOUTH]
COLORS = [(0, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 0)]
EXP=.2

def descaga(r, img):
    r[0] = max(r[0], 0)
    r[1] = max(r[1], 0)
    r[2] = min(r[2], img.shape[1])
    r[3] = min(r[3], img.shape[0])

def expand(r):
    r = list(r)
    w = r[2]-r[0]
    h = r[3]-r[1]
    l = max(w, h)
    r[2] += EXP*l
    r[3] += EXP*l
    r[0] -= EXP*l
    r[1] -= EXP*l
    return tuple(r)

def get_bounding_box(p):
    x1 = 1e100
    y1 = 1e100
    x2 = -1e100
    y2 = -1e100
    for (x, y) in p:
        x1 = min(x1, x)
        x2 = max(x2, x)
        y1 = min(y1, y)
        y2 = max(y2, y)
    return [x1, y1, x2, y2]

def snap_to_grid(r, face):
    cell_width = (face[2] - face[0])/10
    cell_height = cell_width
    r[0] -= face[0]
    r[1] -= face[1]
    r[2] -= face[0]
    r[3] -= face[1]

    r[0] -= r[0] - int(r[0] / cell_width) * cell_width
    r[1] -= r[1] - int(r[1] / cell_height) * cell_height
    r[2] = int((r[2]+cell_width) / cell_width) * cell_width
    r[3] = int((r[3]+cell_height) / cell_height) * cell_height

    r[0] += face[0]
    r[1] += face[1]
    r[2] += face[0]
    r[3] += face[1]

    return list(map(int, r))

def make_square(r):
    w = r[2]-r[0]
    h = r[3]-r[1]
    side = max(w, h)    
    r[0] -= (side-w)/2
    r[1] -= (side-h)/2
    r[2] += (side-w)/2
    r[3] += (side-h)/2
    return list(map(int, r))

parser = argparse.ArgumentParser()
parser.add_argument("image")
parser.add_argument("landmarks")
parser.add_argument("output")
parser.add_argument("txt_output_left_eye")
parser.add_argument("txt_output_right_eye")
parser.add_argument("txt_output_nose")
parser.add_argument("txt_output_mouth")
args = parser.parse_args()

with open(args.landmarks, "r") as f:
    for i in range(3):
        f.readline()
    landmarks = [list(map(float, f.readline().strip("\r\n").split(" ")))
        for i in range(68)]

img = cv2.imread(args.image)

for p in landmarks:
    cv2.circle(img, tuple(map(int, p)), 2, (255, 0, 0), -1)

face_rect = make_square(get_bounding_box([landmarks[i] for i in FACE]))
cv2.rectangle(img, tuple(face_rect[:2]), tuple(face_rect[2:4]), (0, 0, 255),2)

output = (
    args.txt_output_left_eye,
    args.txt_output_right_eye,
    args.txt_output_nose,
    args.txt_output_mouth,
)
for (e, c, fname) in zip(ELEMENTS, COLORS, output):
    p = [landmarks[i] for i in e]
    bb = get_bounding_box(p)
    bb = expand(bb)
    bb = descaga(bb,img)
    bb = tuple(map(int, bb))
    cv2.rectangle(img, tuple(bb[:2]), tuple(bb[2:4]), c,3)
    with open(fname, "w") as f:
        print(args.image, 1, bb[0], bb[1], bb[2], bb[3], file=f)

cv2.imwrite(args.output, img)
