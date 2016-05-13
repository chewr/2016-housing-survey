import googlemaps
import csv
import json
import cPickle as pickle

api_key = ""
try:
	with open("google_apis.key", 'rb') as f:
		api_key = f.read().rstrip()
except:
	print "You need a google api key in a file called 'google_apis.key'"
	exit(1)

clt = googlemaps.Client(key=api_key)

def get_dists(oris, dsts, mode):
	try:
		dists = clt.distance_matrix(oris, dsts, mode=mode)
	except googlemaps.exceptions.Timeout:
		print "Request timed out for " + str(oris) + " to " + str(dsts)
		return None
	except Exception as e:
		print "Routefinding failed for " + str(oris) + " to " + str(dsts)
		return None
	if dists:
		return dists

## max_east = (37.418895, -122.095440)
## max_west = (37.476391, -122.198336)
## max_south = (37.406734, -122.155182)
## max_north = (37.479015, -122.155030)

max_sw = (37.406734,-122.198336)
max_ne = (37.479015,-122.095440)

rng_ew = max_ne[1] - max_sw[1]
rng_ns = max_ne[0] - max_sw[0]

lats = [max_sw[0]]
lngs = [max_sw[1]]
res = 100

ew_step = rng_ew / res
ns_step = rng_ns / res
for i in xrange(res):
	lats.append(lats[-1] + ns_step)
	lngs.append(lngs[-1] + ew_step)

print lats
print lngs

pts = []

for x in lats:
	for y in lngs:
		pts.append((x, y))
slice_size = 40
tmp = None

bike_writer = csv.writer(open("biking_distances.csv", "wb"))
walk_writer = csv.writer(open("walking_distances.csv", "wb"))

fields = ["origin_addr", "dest_addr", "dest_lat", "dest_lng", "duration_secs", "distance_meters"]
bike_writer.writerow(fields)
walk_writer.writerow(fields)

for i in xrange(0, len(pts), slice_size):
	print "Querying slice " + str(i) + " : " + str(i + slice_size)
	w = get_dists(["100 Hamilton Ave, Palo Alto, CA 94301, USA"], pts[i: i + slice_size], "walking")
	# print json.dumps(w, separators=(',', ':'), indent=4)
	if w:
		for ori_idx in xrange(len(w['origin_addresses'])):
			ori = w['origin_addresses'][ori_idx]
			resp_row = w['rows'][ori_idx]['elements']
			for dst_idx in xrange(len(w['destination_addresses'])):
				try:
					dst = w['destination_addresses'][ori_idx]
					entry = resp_row[dst_idx]
					dst_ll = pts[i + dst_idx]
					out = [ori, dst, dst_ll[0], dst_ll[1], entry['duration']['value'], entry['distance']['value']]
					walk_writer.writerow(out)
				except:
					print entry
	else:
		break
	b = get_dists(["100 Hamilton Ave, Palo Alto, CA 94301, USA"], pts[i: i + slice_size], "bicycling")
	if b:
		for ori_idx in xrange(len(b['origin_addresses'])):
			ori = b['origin_addresses'][ori_idx]
			resp_row = b['rows'][ori_idx]['elements']
			for dst_idx in xrange(len(b['destination_addresses'])):
				try:
					dst = b['destination_addresses'][ori_idx]
					entry = resp_row[dst_idx]
					dst_ll = pts[i + dst_idx]
					out = [ori, dst, dst_ll[0], dst_ll[1], entry['duration']['value'], entry['distance']['value']]
					bike_writer.writerow(out)
				except:
					print entry
	else:
		break



