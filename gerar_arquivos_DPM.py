#! /usr/bin/env python3

import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("in_txt")
args = parser.parse_args()

for (i, line) in enumerate(open(args.in_txt, "r")):
    line = line.strip("\r\n").split(" ")
    r = tuple(map(int, line[2:6]))
    img = cv2.imread(line[0])
    #print (line[0])
    with open("%s.txt" % (line[0].split("/")[-1].rsplit(".", 1)[0]), "w") as of:
        print("# McGill Annotation Version 1.00", file=of)
        print("",file=of)
        print("Image filename : \"%s\"" % "/".join(line[0].split("/")[-3:]), file=of)
        print("Image size (X x Y x C) : %d x %d x %d" % (img.shape[1],
                img.shape[0], img.shape[2]), file=of)
        print("Database : \"McGillFaces\"", file=of)
        print("Objects with ground truth : 1 { \"PASinriaperson\" }", file=of)
        print(" ",file=of)        
        print("# Note that there might be other objects in the image",file=of)
        print("# for which ground truth data has not been provided.",file=of)
        print(" ",file=of)
        print("# Top left pixel co-ordinates : (0, 0)",file=of)
        print("",file=of)
        print("# Details for object 1 ('PASinriaperson')",file=of)
        print("# Center point -- not available in other PASCAL databases -- refers",file=of)
        print("# to person head center",file=of)
        print("Original label for object",
            "1 \"PASinriaperson\" : \"UprightPerson\"", file=of)
        print("Center point on object 1 \"PASinriaperson\" (X, Y) : (%d, %d)"
            % (r[0]+r[2]/2, r[1]+r[3]/2), file=of)
        print("Bounding box for object 1 \"PASinriaperson\"",
            "(Xmin, Ymin) - (Xmax, Ymax) : (%d, %d) - (%d, %d)"
            % (r[0], r[1], r[0]+r[2], r[1]+r[3]), file=of)

#print("Image filename : \"%s\"" % (line[0]), file=of)
