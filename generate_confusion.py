#! /bin/env python3

import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if len(sys.argv) < 4:
    print("Usage: %s TEST_FILE PREDICTIONS OUTPUT" % (sys.argv[0]),
        file=sys.stderr)
    sys.exit(1)


predictions = open(sys.argv[2], "r")
test_file = open(sys.argv[1], "r")

classes = predictions.readline()[:-1].split(" ")[1:]

for i in range(len(classes)):
    classes[i] = float(classes[i])

sorted_classes = classes.copy()
sorted_classes.sort()
rev_classes = {}
for c in sorted_classes:
    rev_classes[c] = len(rev_classes)

confusion = [[0] * len(classes) for i in range(len(classes))]

ok = 0
total = 0

for l in predictions:
    total+=1
    l = l.split(" ")
    for i in range(len(l)):
        l[i] = float(l[i])
    truth = float(test_file.readline().split(" ")[0])

    confusion[rev_classes[truth]][rev_classes[l[0]]] += 1
    if truth == l[0]:
        ok += 1

normalization = [sum(r) for r in confusion]
for i in range(len(confusion)):
    confusion[i] = list(map(lambda x: x/normalization[i] if normalization[i]
            else 0, confusion[i]))

predictions.close()
test_file.close()

plt.matshow(confusion)
plt.title("%.2f%% Accuracy" % (ok*100/total))
plt.ylabel("Truth")
plt.xlabel("Prediction")
plt.xticks(range(len(sorted_classes)), [int(i) for i in sorted_classes])
plt.yticks(range(len(sorted_classes)), [int(i) for i in sorted_classes])

for i in range(len(confusion)):
    for j in range(len(confusion[i])):
        if confusion[i][j] >= 0.001:
            plt.text(j-.45, i+.2, "%.1f" % (confusion[i][j]*100), fontsize=9)

plt.show()
plt.savefig(sys.argv[3])
