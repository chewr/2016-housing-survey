import csv
import json
from sets import Set

wd = csv.reader(open("walking_distances.csv", "rb"))
wd.next()

bd = csv.reader(open("biking_distances.csv", "rb"))
bd.next()

## inner shire
inner_shire_str = Set([])
for row in wd:
 	if int(row[4]) < 1200:
		inner_shire_str.add((row[2], row[3]))

## outer shire
outer_shire_str = Set([])
for row in bd:
	if int(row[4]) < 900:
		sll = (row[2], row[3])
		if sll not in inner_shire_str:
			# print "Outer shire: " + row[1]
			outer_shire_str.add(sll)

## floatify
inner_shire = []
for fll in inner_shire_str:
	inner_shire.append((float(fll[0]), float(fll[1])))

outer_shire = []
for fll in outer_shire_str:
	outer_shire.append((float(fll[0]), float(fll[1])))

out = { "inner_shire" : inner_shire, "outer_shire": outer_shire }
out_str = json.dumps(out, separators=(',', ':'), indent=4)

f = open("shires.json", 'wb')
f.write(out_str)
