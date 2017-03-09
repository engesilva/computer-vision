#! /usr/bin/env python3

import sys


for l in sys.stdin:
  l = l.strip("\r\n").split(" ")
  r = list(map(int, l[2:6]))
  print(l[0], l[1], r[0], r[1], r[2]-r[0], r[3]-r[1])
