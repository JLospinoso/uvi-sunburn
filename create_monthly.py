import csv
import numpy

with open("uvi-cut.csv") as x:
    uvi = list(csv.reader(x))
    print "Read %u uvi lines" % len(uvi)


with open("google-cut.csv") as x:
    google = list(csv.reader(x))
    print "Read %u google lines" % len(google)

google_lookup = {}
for x in google[1:]:
    key = "%s %s %s" % (x[0], x[3], x[5])
    if key in google_lookup:
        google_lookup[key].append(x)
    else:
        google_lookup[key] = [x]

uvi_lookup = {}
for x in uvi[1:]:
    key = "%s %s %s" % (x[4], x[1], x[3])
    if key in uvi_lookup:
        uvi_lookup[key].append(x)
    else:
        uvi_lookup[key] = [x]

joint_keys = set(uvi_lookup.keys()).intersection(google_lookup.keys())

def extract_mean(x, col):
    return numpy.mean(map(lambda y: float(y[col]), x))

with open("monthly-cut.csv", "wb") as f:
    out = csv.writer(f)
    print google[0]
    print uvi[0]
    out.writerow(['state', 'month', 'year', 'search', 'clear_uvi', 'cloudy_uvi', 'cloud_trans', 'sz_angle', 'aerosol_trans', 'tc_ozone'])
    for key in joint_keys:
        g = google_lookup[key]
        u = uvi_lookup[key]
        state = g[0][0]
        month = g[0][3]
        year = g[0][5]
        search = extract_mean(g, 6)
        clear_uvi = extract_mean(u, 6)
        cloudy_uvi = extract_mean(u, 7)
        cloud_trans = extract_mean(u, 8)
        sz_angle = extract_mean(u, 9)
        aerosol_trans = extract_mean(u, 10)
        tc_ozone = extract_mean(u, 11)
        out.writerow([state, month, year, search, clear_uvi, cloudy_uvi, cloud_trans, sz_angle, aerosol_trans, tc_ozone])
