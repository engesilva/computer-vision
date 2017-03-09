#! /usr/bin/env python3

import argparse

AX=5
AY=4

def cmpf(a, b):
    if abs(a-b) < 1e-9:
        return 0
    return 1 if a > b else -1

def get_intersection(a, b):
    p1 = (max(a[0], b[0]), max(a[1], b[1]))
    p2 = (min(a[0]+a[2], b[0]+b[2]), min(a[1]+a[3], b[1]+b[3]))

    return (p1[0], p1[1], max(p2[0]-p1[0], 0), max(p2[1]-p1[1], 0))

def intersection_coefficient(a, b):
    intersection = get_intersection(a, b)
    intersection_area = intersection[2]*intersection[3]
    a_area = a[2]*a[3]
    b_area = b[2]*b[3]

    return intersection_area/max(a_area, b_area)

parser = argparse.ArgumentParser()
parser.add_argument("ground_truth")
parser.add_argument("detections")
parser.add_argument("-p", "--p2", action="store_true")
parser.add_argument("-f", "--filter")
parser.add_argument("-g", "--graph-data")
parser.add_argument("-l", "--limit", action="store_true")
parser.add_argument("-m", "--maximize", action="store_true")
parser.add_argument("-a", "--artificial-face", action="store_true")
args = parser.parse_args()

fregion = None
if args.filter is not None:
    fregion = [tuple(map(int, args.filter.split(",")))]
    if len(fregion) != 4:
        raise ValueError
    if args.p2:
        fregion = (fregion[0], fregion[1],
            fregion[2]-fregion[0], fregion[3]-fregion[1])
    if fregion[2] < 0 or fregion[3] < 0:
        raise ValueError

gts = {l.split(" ")[0] : tuple(map(int, l.split(" ")[2:6]))
    for l in open(args.ground_truth, "r")}

total = 0
fps = 0
ok = 0
valid = 0
ics = []
for line in open(args.detections, "r"):
    l = list(filter(None, line.strip("\r\n").split(" ")))

    expected_detections = int(l[1])
    if len(l) != expected_detections*4 + 2:
        print("Invalid line:\n", l)
        continue
    valid += 1

    detections = [tuple(map(int, l[i:i+4])) for i in range(2, len(l), 4)]
    if args.p2:
        detections = [(d[0], d[1], d[2]-d[0], d[3]-d[1]) for d in detections]
    if args.artificial_face:
        n = gts[l[0]]
        fregion = (n[0]-n[2]*(AX-1)//2, n[1]-n[3]*(AY-1)//2, n[2]*AX, n[3]*AY)
    if fregion is not None:
        detections = list(filter(lambda r:
                r[0] >= fregion[0] and r[1] >= fregion[1]
                and r[0]+r[2] <= fregion[0]+fregion[2]
                and r[1]+r[3] <= fregion[1]+fregion[3], detections))
    if args.maximize:
        best = -1e100
        nd = []
        for d in detections:
            if not d[2] or not d[3]:
                continue
            c = intersection_coefficient(d, gts[l[0]])
            if c > best:
                best = c
                nd = [d]
        detections = nd
    elif args.limit:
        detections = detections[:1]
    line_ok = False
    if not len(detections) or (not detections[0][2] and not detections[0][3]):
        ics.append(0)
    else:
        ics.append(intersection_coefficient(detections[0], gts[l[0]]))
    for d in detections:
        if not d[2] or not d[3]:
            continue
        total += 1
        c = intersection_coefficient(d, gts[l[0]])
        if cmpf(c, 0.5) >= 0:
            line_ok = True
        else:
            fps += 1
    if line_ok:
        ok += 1

ics.sort()
sxy = []
last = None
for (i, ic) in enumerate(ics):
    if last is None or cmpf(last, ic):
        sxy.append((ic, 1-(i+1)/len(ics)))
    else:
        sxy[-1] = (ic, 1-(i+1)/len(ics))
    last = ic

if args.graph_data is not None:
    with open(args.graph_data, "w") as f:
        for (x, y) in sxy:
            print(x, y, file=f)

print("OK: %f%%\nFP: %f%%" % (ok/valid*100, fps/total*100))
