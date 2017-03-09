#! /usr/bin/env python2

import cv2
import sys

#ler o arquivo txt com as coordenadas dos bounding box do nariz
#img = cv2.imread(sys.argv[1])
f = open(sys.argv[1], "r")

i = 0
for (i, line) in enumerate(f):
   i += 1
   line = line.strip("\r\n").split(" ")
   rect = list(map(int, line[2:6]))
   img = cv2.imread(line[0])
   cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 0, 255),3)
   cv2.imwrite("%d.png" %  i, img)
