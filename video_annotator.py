#! /usr/bin/env python3

import argparse
import cv2

CTRL = 262144
SHIFT = 65536
LEFT_ARROW = 65361
UP_ARROW = 65362
RIGHT_ARROW = 65363
DOWN_ARROW = 65364

parser = argparse.ArgumentParser()
parser.add_argument("txt")
args = parser.parse_args()

def read_file(fpath):
    r = []
    for line in open(fpath, "r"):
        line = line.strip("\r\n").split(" ")
        if len(line) == 1:
            r.append([line[0], None])
        else:
            rect = list(map(int, line[-4:]))
            r.append([line[0], rect])
    return r

def save_file(fpath, data):
    with open(fpath, "w") as f:
        for (img, rect) in data:
            if rect is None:
                print(img, file=f)
            else:
                print(img, 1, rect[0], rect[1], rect[2], rect[3], file=f)


data = read_file(args.txt)
pos = 0
last = [-1, -1, -1, -1]
done = False
if data[pos][1] is None:
    data[pos][1] = last
img = cv2.imread(data[pos][0])
while not done:
    if pos == len(data):
        break
    s = img.copy()
    if data[pos][1] is not None:
        cv2.rectangle(s,
            (data[pos][1][0], data[pos][1][1]),
            (data[pos][1][0]+data[pos][1][2], data[pos][1][1]+data[pos][1][3]),
            (0, 0, 255), 1)
    cv2.imshow("img", s)
    print("%d/%d" % (pos+1, len(data)))
    while True:
        key = cv2.waitKey(0)
        mul = 10 if key & SHIFT else 1
        if key == -1 or key & 0xff == 27:
            done = True
            break
        elif key & 0xff == ord("d"):
            data[pos][1] = [-1, -1, -1, -1]
            break
        elif key & 0xff == ord("r"):
            data[pos][1] = [l for l in last]
            break
        elif key & 0xff == ord("n"):
            if data[pos][1][0] == -1 or data[pos][1] is None:
                data[pos][1] = [32, 32, 32, 32]
            break
        elif key & 0xff in (ord("k"), ord("x")):
            if pos < len(data)-1:
                last = data[pos][1]
                pos += 1
                img = cv2.imread(data[pos][0])
                if data[pos][1] is None:
                    data[pos][1] = [l for l in last]
            break
        elif key & 0xff in (ord("j"), ord("z")):
            if pos > 0:
                last = data[pos][1]
                pos -= 1
                img = cv2.imread(data[pos][0])
                if data[pos][1] is None:
                    data[pos][1] = [l for l in last]
            break
        if data[pos][1] is None or data[pos][1][0] == -1:
            continue
        if key & 0xffff == LEFT_ARROW:
            if key & CTRL:
                data[pos][1][2] -= mul
            else:
                data[pos][1][0] -= mul
            break
        elif key & 0xffff == RIGHT_ARROW:
            if key & CTRL:
                data[pos][1][2] += mul
            else:
                data[pos][1][0] += mul
            break
        elif key & 0xffff == UP_ARROW:
            if key & CTRL:
                data[pos][1][3] -= mul
            else:
                data[pos][1][1] -= mul
            break
        elif key & 0xffff == DOWN_ARROW:
            if key & CTRL:
                data[pos][1][3] += mul
            else:
                data[pos][1][1] += mul
            break
    if data[pos][1] is not None and data[pos][1] != [-1, -1, -1, -1]:
        data[pos][1][0] = max(data[pos][1][0], 0)
        data[pos][1][1] = max(data[pos][1][1], 0)
        data[pos][1][2] = min(data[pos][1][2], img.shape[1]-data[pos][1][0])
        data[pos][1][2] = max(data[pos][1][2], 1)
        data[pos][1][3] = min(data[pos][1][3], img.shape[0]-data[pos][1][1])
        data[pos][1][3] = max(data[pos][1][3], 1)
    save_file(args.txt, data)
