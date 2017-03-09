#! /usr/bin/env python3

import cv2
import argparse
import math
from scipy import stats

def intersection(r1, r2):
    x = (r2[1]-r1[1])/(r1[0]-r2[0])
    return (x, r1[0]*x + r1[1])

parser = argparse.ArgumentParser()
parser.add_argument("csv")
parser.add_argument("out_img")
args = parser.parse_args()

with open(args.csv, "r") as f:
    img_path = f.readline().strip("\r\n")
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    rect = tuple(map(float, f.readline().strip("\r\n").split(",")))
    pose = tuple(map(float, f.readline().strip("\r\n").split(",")))
    for line in f:
        lms = [tuple(map(float, v.split(":"))) if v != "" else (-1, -1)
            for v in line.strip("\r\n").split(",")]
        for (i, lm) in enumerate(lms):
            cv2.circle(img, tuple(map(int, lm[:2])), 2, (0, 0, 255))
            cv2.putText(img, "%d" % (i+1), (int(lm[0]-5), int(lm[1]-5)),
                cv2.FONT_ITALIC, .5, (0, 255, 0))

        eyeline = []
        for p in lms[6:12]:
            if p != (-1, -1):
                eyeline.append(p)
        if len(eyeline) < 2:
            for p in lms[17:20]:
                if p != (-1, -1):
                    eyeline.append(p)
        if len(eyeline) <= 2:
            eyeline *= 2
        (a, _, _, _, _) = stats.linregress(eyeline)
        a = [a, -1/a if a else img.shape[0],
            a, -1/a if a else img.shape[0]]
        b = [0, 0, 0, 0]
        for i in range(2):
            b[i] = max([-a[i]*p[0] + p[1]
                for p in lms[17:20] if p != (-1, -1)])
        for i in range(2, 4):
            b[i] = min([-a[i]*p[0] + p[1]
                for p in lms[17:20] if p != (-1, -1)])

        w = b[3]-b[1]

        for (ra, rb) in zip(a, b):
            cv2.line(img, (0, int(rb)),
                (img.shape[1], int(img.shape[1]*ra+rb)), (255, 0, 255))

        limits = [
            intersection((a[0], b[0]), (a[1], b[1])),
            intersection((a[0], b[0]), (a[3], b[3])),
            intersection((a[2], b[2]), (a[1], b[1])),
            intersection((a[2], b[2]), (a[3], b[3])),
        ]

        r = [
            min([x for (x, _) in limits]),
            min([y for (_, y) in limits]),
            max([x for (x, _) in limits]),
            max([y for (_, y) in limits]),
        ]

        w = r[2]-r[0]
        if lms[17] != (-1, -1):
            r[0] -= .15*w
        else:
            r[0] -= .35*w
        if lms[19] != (-1, -1):
            r[2] += .15*w
        else:
            r[2] += .35*w
        w = r[2]-r[0]

        r[3] += .3*w
        r[1] = r[3]-w/2

        r = tuple(map(int, r))
        cv2.rectangle(img, r[:2], r[2:4], (255, 0, 0))
        rect = tuple(map(int, rect))
        print(img_path, 1, r[0], r[1], r[2], r[3])
           # rect[0], rect[1], rect[2], rect[3])
if args.out_img != "/dev/null":
    cv2.imwrite(args.out_img, img)
