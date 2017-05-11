import os

city_map = {}
print "[*] Parsing cities"
with open("data/cities.lst") as cities_file:
    for line in cities_file:
        (code, state) = (line[46:49].lower(), line[21:23].lower())
        city_map[code] = state

google_dir = "data/google/"
with open("google.csv", "w") as out:
    out.write("state,mode,date,month,day,year,value\n")
    print "[*] Reading search data from " + google_dir
    for state_file in os.listdir(google_dir):
        state_file_abv = state_file[0:2].lower()
        state_file_path = "%s/%s" % (google_dir, state_file)
        print "[ ] %s" % state_file_path
        with open(state_file_path) as data:
            data.next()     # Web Search interest: sunburn
            data.next()     # Texas (United States) 2004 - present
            data.next()     #
            data.next()     # Interest over time
            header = data.next().split(",")
            mode = header[0].lower()
            for x in data:
                if x == "\n":
                    break
                line = x.split(",")
                (month, day, year) = (0, 0, 0)
                if mode == "week":
                    year = int(x[0:4])
                    month = int(x[5:7])
                    day = int(x[8:11])
                elif mode == "month":
                    year = int(x[0:4])
                    month = int(x[5:7])
                    day = 1
                value_token = line[1]
                if value_token == " \n" or value_token == "\n":
                    break
                value = float(value_token)
                out.write("%s," % state_file_abv)
                out.write("%s," % mode)
                out.write("%u/%u/%u," % (month, day, year))
                out.write("%u," % month)
                out.write("%u," % day)
                out.write("%u," % year)
                out.write("%f" % value)
                out.write("\n")

with open("uvi.csv", "w") as out:
    out.write("date,month,day,year,state,station,clear_uvi,cloudy_uvi,cloud_trans,sz_angle,aerosol_trans,tc_ozone\n")
    noaa_dir = "data/noaa/"
    print "[*] Reading years from " + noaa_dir
    for year_dir in os.listdir(noaa_dir):
        print "[ ] Directory: %s" % year_dir
        for loc_file in os.listdir(noaa_dir + year_dir):
            loc_file_abv = loc_file[0:3].lower()
            file_path = "%s/%s/%s" % (noaa_dir, year_dir, loc_file)
            state_code = city_map[loc_file_abv]
            print "[ ] %s (%s)" % (file_path, state_code)
            with open(file_path) as data:
                for x in data:
                    year = int(x[5:9])
                    month = int(x[9:11])
                    day = int(x[11:13])
                    out.write("%u/%u/%u," % (month, day, year))
                    out.write("%u," % month)
                    out.write("%u," % day)
                    out.write("%u," % year)
                    out.write("%s," % state_code)
                    out.write("%s," % x[1:4].lower())
                    out.write("%f," % float(x[13:19]))
                    out.write("%f," % float(x[19:25]))
                    out.write("%f," % float(x[25:31]))
                    out.write("%f," % float(x[31:37]))
                    out.write("%f," % float(x[37:43]))
                    out.write("%f" % float(x[43:49]))
                    out.write("\n")
