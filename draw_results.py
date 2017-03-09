#! /usr/bin/env python3

import cv2

import sys

for (n, line) in enumerate(sys.stdin):
    line = line.strip("\r\n").split(" ")
    img = cv2.imread(line[0])
    ok = False
    for i in range(2, len(line), 4):
        r = tuple(map(int, line[i:i+4]))
        cv2.rectangle(img, r[:2], r[2:4], (0, 0, 255))
        ok = True
    if ok:
        cv2.imwrite("%07d.jpg" % (n+1), img)
