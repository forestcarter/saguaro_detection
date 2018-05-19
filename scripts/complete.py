import os
import math
import arcpy
from arcpy.sa import *
import datetime
import Pysolar.solar
arcpy.env.overwriteOutput = True
locallat=(32.287117)
locallong=(360-111.166215)
angleDiff=10
#abPath=(os.path.dirname(os.path.realpath(__file__)))[:-8]
abPath=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#Part 1
if arcpy.GetParameterAsText(0)=='':
    print('no params')
    #abPath=os.path.join("c:"+os.sep, "Users","Forest", "Desktop", "saguaro_detection_git")
    #abPath=os.path.join("f:"+os.sep,"saguaro_detection_git")
    dem = os.path.join(abPath, "dem", "largedem")
    SNPBoundaries_shp = os.path.join(abPath, "snp_boundary", "SNPBoundaries.shp")
    flightpoints = os.path.join(abPath, "Ortho2011_FlightPoints", "Pima_Photos_2011.shp")
    trsfile =  os.path.join(abPath, "township_range_az", "trs.shp")
    imageFolder = os.path.join(abPath, "PAG_2011_6inchOrtho")
    shadowwidth = 2
    shadowlength = 10
    maxelev = 1550
    intermediateFolder = os.path.join(abPath, "outputs","intermediate")
    finishedFolder = os.path.join(abPath, "outputs","finished")

else:
    dem = arcpy.GetParameterAsText(0)
    #SNPBoundaries_shp = arcpy.GetParameterAsText(1)
    flightpoints = arcpy.GetParameterAsText(1)
    trsfile = arcpy.GetParameterAsText(2)
    imageFolder = arcpy.GetParameterAsText(3)
    shadowwidth = int(arcpy.GetParameterAsText(4))
    shadowlength = int(arcpy.GetParameterAsText(5))
    maxelev= arcpy.GetParameterAsText(6)
    intermediateFolder = arcpy.GetParameterAsText(7)
    finishedFolder = arcpy.GetParameterAsText(8)

fpoutput = os.path.join(intermediateFolder, "fp_sun_angles.shp")
merged_shp = os.path.join(intermediateFolder, "merged.shp")
saguarosPoints =  os.path.join(intermediateFolder,"merged_clipped.shp")
pointsWithElevation = os.path.join(intermediateFolder,"pts_with_elev.shp")


if os.path.isdir(intermediateFolder):
    os.system('rmdir /s /q {}'.format(intermediateFolder))
    print("removed intermediate")
os.system('mkdir {}'.format(intermediateFolder))

# Process: Spatial Join
arcpy.SpatialJoin_analysis(flightpoints, trsfile, fpoutput, "JOIN_ONE_TO_ONE", "KEEP_ALL", "Date_ \"Date_\" true true false 10 Long 0 10 ,First,#,{0},Date_,-1,-1;GPSTime \"GPSTime\" true true false 19 Double 0 0 ,First,#,{0},GPSTime,-1,-1;TOWNSHIP \"TOWNSHIP\" true true false 4 Text 0 0 ,First,#,{1},TOWNSHIP,-1,-1;RANGE \"RANGE\" true true false 4 Text 0 0 ,First,#,{1},RANGE,-1,-1;SECTION \"SECTION\" true true false 2 Text 0 0 ,First,#,{1},SECTION,-1,-1".format(flightpoints,trsfile), "INTERSECT", "", "")

# Process: Add Field
arcpy.AddField_management(fpoutput, "az2", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (2)
arcpy.AddField_management(fpoutput, "eastwest", "STRING", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (3)
arcpy.AddField_management(fpoutput, "TILE_NAME", "STRING", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (4)
arcpy.AddField_management(fpoutput, "localhour", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

finames=['GPSTime', 'Date_', 'az2','eastwest', 'TILE_NAME','TOWNSHIP','RANGE','SECTION','localhour']
rows = arcpy.da.UpdateCursor(fpoutput,finames)
for row in rows:
    hourraw=(row[0]%(3600*24))/3600
    hour=int(hourraw)
    day=str(row[1])
    year=day[:4]
    month=day[4:6]
    dayy=day[6:]
    minute=60*(hourraw-hour)
    myangle = Pysolar.solar.GetAzimuth(locallat,locallong,datetime.datetime(int(year), int(month), int(dayy), int(hour), int(minute)))
    row[2]=myangle
    if myangle<-180:
        row[3]='w'
    else:
        row[3]='e'
    myt = str(row[5])
    myr = str(row[6])
    mys = str(row[7])
    row[8] = hourraw-7

    row[4]='E'+myt[:2]+myr[:2]+mys
    rows.updateRow(row)

del row
del rows

#Part 2
arcpy.CheckOutExtension('Spatial')

os.chdir(intermediateFolder)
arcpy.env.scratchWorkspace = intermediateFolder
arcpy.env.workspace = intermediateFolder
arcpy.env.overwriteOutput = True

print 'begin'
def buildBlankKernal():
    blankKernal = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    return blankKernal
# Begin Kernal function
def buildkernal(rawangle, intermediateFolder, shadowwidth, shadowlength):
    os.chdir(intermediateFolder)
    kernalcomplete = buildBlankKernal()
    width = shadowwidth
    length = shadowlength
    shiftfactor = width * 2
    halfwidth = width / 2

    degreeangle = abs(rawangle)

    if degreeangle > 180:
        degreeangle = 360 - degreeangle

    radianangle = degreeangle * (math.pi / 180)
    slope = 1 / (math.tan(radianangle))
    xatymin = (math.cos(radianangle)) * (width / 2)
    ymin = -(math.sin(radianangle)) * (width / 2)
    xmin = (-xatymin)
    # movetoshadfile
    shiftx = math.sin(radianangle) * shiftfactor
    shifty = shiftx * slope
    kernalcomplete[int(round(9 - shifty))][int(round(shiftx + 9))] = 1

    f = open("shifttoshade.txt", "w")
    f.write('19 19\n')
    stingwrite = ''
    for xyz in xrange(19):

        for mmm in xrange(19):

            stingwrite = stingwrite + '{}'.format(kernalcomplete[xyz][mmm])
            if mmm < 18:
                stingwrite = stingwrite + ' '
            if mmm == 18 and xyz != 18:
                stingwrite = stingwrite + '\n'

        f.write(stingwrite)
        stingwrite = ''

    f.close()
    kernalcomplete[int(round(9 - shifty))][int(round(shiftx + 9))] = 0

    # movebackfile
    shiftx = math.sin(radianangle) * shiftfactor
    shifty = shiftx * slope
    kernalcomplete[int(round(9 + shifty))][int(round(9 - shiftx))] = 1

    f = open("shiftbacke.txt", "w")
    f.write('19 19\n')
    stingwrite = ''
    for xyz in xrange(19):

        for mmm in xrange(19):

            stingwrite = stingwrite + '{}'.format(kernalcomplete[xyz][mmm])
            if mmm < 18:
                stingwrite = stingwrite + ' '
            if mmm == 18 and xyz != 18:
                stingwrite = stingwrite + '\n'

        f.write(stingwrite)
        stingwrite = ''
    f.close()
    kernalcomplete[int(round(9 + shifty))][int(round(9 - shiftx))] = 0

    # shadowfile-----------------------
    for y in xrange(-9, 10):
        for x in xrange(-9, 10):
            if y < (slope * x + halfwidth / math.sin(radianangle) + 0.5) and y > (
                                slope * x - halfwidth / math.sin(radianangle) + 0.5) and y > (
                        -1 / slope) * x + 0.5 and y < (
                            (-1 / slope) * x + length / (math.cos(radianangle))):
                changey = 9 - y
                changex = x + 9
                kernalcomplete[changey][changex] = 1

    # write kernal to file
    f = open("customke.txt", "w")
    f.write('19 19\n')
    stingwrite = ''
    for xyz in xrange(19):
        for mmm in xrange(19):
            stingwrite = stingwrite + '{}'.format(kernalcomplete[xyz][mmm])
            if mmm < 18:
                stingwrite = stingwrite + ' '
            if mmm == 18 and xyz != 18:
                stingwrite = stingwrite + '\n'

        f.write(stingwrite)
        stingwrite = ''
    f.close()
    # end shadow file-----------------------
    # above file------------------------------------------
    #kernalcomplete = [([0]*19)]*19
    kernalcomplete = buildBlankKernal()
    for y in xrange(-9, 10):
        for x in xrange(-9, 10):
            if y > (slope * x + halfwidth / math.sin(radianangle) + 0.5) and y < (
                                slope * x + (3 * halfwidth) / math.sin(radianangle) + 0.5) and y > (
                        -1 / slope) * x + 0.5 and y < ((-1 / slope) * x + length / (math.cos(radianangle))):
                changey = 9 - y
                changex = x + 9

                kernalcomplete[changey][changex] = 1

    # write kernal to file
    f = open("customkabovee.txt", "w")
    f.write('19 19\n')
    stingwrite = ''
    for xyz in xrange(19):
        for mmm in xrange(19):
            stingwrite = stingwrite + '{}'.format(kernalcomplete[xyz][mmm])
            if mmm < 18:
                stingwrite = stingwrite + ' '
            if mmm == 18 and xyz != 18:
                stingwrite = stingwrite + '\n'

        f.write(stingwrite)
        stingwrite = ''

    f.close()
    # end above file------------------------------------------
    #kernalcomplete = [([0]*19)]*19
    kernalcomplete = buildBlankKernal()
    # below file------------------------------------------
    for y in xrange(-9, 10):
        for x in xrange(-9, 10):
            if y > (slope * x - (3 * halfwidth) / math.sin(radianangle) + 0.5) and y < (
                                slope * x - halfwidth / math.sin(radianangle) + 0.5) and y > (
                        -1 / slope) * x + 0.5 and y < (
                            (-1 / slope) * x + length / (math.cos(radianangle))):
                changey = 9 - y
                changex = x + 9
                kernalcomplete[changey][changex] = 1
    # write kernal to file
    f = open("customkbelowe.txt", "w")
    f.write('19 19\n')
    stingwrite = ''
    for xyz in xrange(19):

        for mmm in xrange(19):

            stingwrite = stingwrite + '{}'.format(kernalcomplete[xyz][mmm])
            if mmm < 18:
                stingwrite = stingwrite + ' '
            if mmm == 18 and xyz != 18:
                stingwrite = stingwrite + '\n'

        f.write(stingwrite)
        stingwrite = ''
    f.close()
    # makesw

    kernalsmall = [0, 0, 0], [1, 9, 0], [1, 1, 0]
    f = open("se.txt", "w")
    f.write('3 3\n')
    stingwrite = ''
    for xyz in xrange(3):

        for mmm in xrange(3):

            stingwrite = stingwrite + '{}'.format(kernalsmall[xyz][mmm])
            if mmm < 2:
                stingwrite = stingwrite + ' '
            if mmm == 2 and xyz != 2:
                stingwrite = stingwrite + '\n'

        f.write(stingwrite)
        stingwrite = ''
    f.close()

    # makese
    kernalsmall = [0, 0, 0], [0, 9, 1], [0, 1, 1]
    f = open("sw.txt", "w")
    f.write('3 3 \n')
    stingwrite = ''
    for xyz in xrange(3):

        for mmm in xrange(3):

            stingwrite = stingwrite + '{}'.format(kernalsmall[xyz][mmm])
            if mmm < 2:
                stingwrite = stingwrite + ' '
            if mmm == 2 and xyz != 2:
                stingwrite = stingwrite + '\n'

        f.write(stingwrite)
        stingwrite = ''

    f.close()
    # end below file------------------------------------------

    # Begin flipping-----------------------------------------------------------
    if abs(rawangle) > 180:
        os.chdir(intermediateFolder)

        # flip shadshift
        f = open("{}\\shifttoshadw.txt".format(intermediateFolder), "w")
        my_file = open("shifttoshade.txt")

        biglist = my_file.readlines()

        masterlist = []
        for xvar in xrange(1, 20):
            linelist = biglist[xvar].split()

            for y in xrange(19):
                if y <= 8:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '8'

                if y >= 10:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '1'

                    if linelist[y] == '8':
                        linelist[y] = 1

            masterlist.append(linelist)

        f.write(str(biglist[0]))

        for xyz in xrange(19):
            for mmm in xrange(19):
                if mmm == 18:
                    joy = str(masterlist[xyz][mmm])
                else:
                    joy = str(masterlist[xyz][mmm]) + ' '

                f.write(joy)

            if xyz == 18 and mmm == 18:
                pass
            else:
                f.write('\n')

        f.close()
        my_file.close()

        # flip shiftback
        f = open("{}\\shiftbackw.txt".format(intermediateFolder), "w")
        my_file = open("shiftbacke.txt")
        biglist = my_file.readlines()

        masterlist = []
        for xvar in xrange(1, 20):
            linelist = biglist[xvar].split()

            for y in xrange(19):
                if y <= 8:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '8'

                if y >= 10:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '1'

                    if linelist[y] == '8':
                        linelist[y] = 1

            masterlist.append(linelist)

        f.write(str(biglist[0]))

        for xyz in xrange(19):
            for mmm in xrange(19):
                if mmm == 18:
                    joy = str(masterlist[xyz][mmm])
                else:
                    joy = str(masterlist[xyz][mmm]) + ' '

                f.write(joy)

            if xyz == 18 and mmm == 18:
                pass
            else:
                f.write('\n')

        f.close()
        my_file.close()

        # flip shadow
        f = open("{}\\customkw.txt".format(intermediateFolder), "w")
        my_file = open("customke.txt")

        biglist = my_file.readlines()

        masterlist = []
        for xvar in xrange(1, 20):
            linelist = biglist[xvar].split()

            for y in xrange(19):
                if y <= 8:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '8'

                if y >= 10:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '1'

                    if linelist[y] == '8':
                        linelist[y] = 1

            masterlist.append(linelist)

        f.write(str(biglist[0]))

        for xyz in xrange(19):
            for mmm in xrange(19):
                if mmm == 18:
                    joy = str(masterlist[xyz][mmm])
                else:
                    joy = str(masterlist[xyz][mmm]) + ' '

                f.write(joy)

            if xyz == 18 and mmm == 18:
                pass
            else:
                f.write('\n')

        f.close()
        my_file.close()
        # flip above
        f = open("{}\\customkabovew.txt".format(intermediateFolder), "w")
        my_file = open("customkabovee.txt")

        biglist = my_file.readlines()

        masterlist = []
        for xvar in xrange(1, 20):
            linelist = biglist[xvar].split()

            for y in xrange(19):
                if y <= 8:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '8'

                if y >= 10:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '1'

                    if linelist[y] == '8':
                        linelist[y] = 1

            masterlist.append(linelist)

        f.write(str(biglist[0]))

        for xyz in xrange(19):
            for mmm in xrange(19):
                if mmm == 18:
                    joy = str(masterlist[xyz][mmm])
                else:
                    joy = str(masterlist[xyz][mmm]) + ' '

                f.write(joy)

            if xyz == 18 and mmm == 18:
                pass
            else:
                f.write('\n')

        f.close()
        my_file.close()
        # flip below
        f = open("{}\\customkbeloww.txt".format(intermediateFolder), "w")
        my_file = open("customkbelowe.txt")

        biglist = my_file.readlines()

        masterlist = []
        for xvar in xrange(1, 20):
            linelist = biglist[xvar].split()

            for y in xrange(19):
                if y <= 8:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '8'

                if y >= 10:

                    if linelist[y] == '1':

                        newpos = 18 - y
                        if linelist[newpos] != '1':
                            linelist[y] = '0'

                        linelist[newpos] = '1'

                    if linelist[y] == '8':
                        linelist[y] = 1

            masterlist.append(linelist)

        f.write(str(biglist[0]))

        for xyz in xrange(19):
            for mmm in xrange(19):
                if mmm == 18:
                    joy = str(masterlist[xyz][mmm])
                else:
                    joy = str(masterlist[xyz][mmm]) + ' '

                f.write(joy)

            if xyz == 18 and mmm == 18:
                pass
            else:
                f.write('\n')

        f.close()
        my_file.close()
        # end kernal function
def finddist(clatoshad_14, dir, path):
    path2 = path
    # Local variables:
    points_shp = "{}\\points.shp".format(path2)
    dist1 = "{}\\dist1".format(path2)
    # Process: Raster to Point
    arcpy.RasterToPoint_conversion(clatoshad_14, points_shp, "VALUE")
    # Process: Add XY Coordinates
    arcpy.AddXY_management(points_shp)
    # Process: Add Field
    arcpy.AddField_management(points_shp, "distfield", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    xlist = []
    ylist = []
    finames = ['POINT_X', 'POINT_Y', 'distfield']
    rows = arcpy.da.UpdateCursor(points_shp, finames)
    for row in rows:
        xlist.append(row[0])
        ylist.append(row[1])
    rows.reset()
    for row in rows:
        if dir == 'e':
            changex = row[0] - min(xlist)
            changey = row[1] - min(ylist)
            row[2] = math.sqrt(changex * changex + changey * changey)
        if dir == 'w':
            changex = row[0] - max(xlist)
            changey = row[1] - min(ylist)
            row[2] = math.sqrt(changex * changex + changey * changey)
        rows.updateRow(row)
    del row
    del rows
    arcpy.PointToRaster_conversion(points_shp, "distfield", dist1, "MOST_FREQUENT", "NONE", clatoshad_14)
    return dist1

cursor = arcpy.da.SearchCursor(fpoutput, ["eastwest", "TILE_NAME", 'az2'])
cursor.reset()

# look at exisiting point shapefiles
largefilelist = []
finishedpoints = []
for filename3 in (os.listdir(finishedFolder)):
    idnum = "{}S{}E{}".format(filename3[0:2], filename3[2:4], filename3[4:6])
    finishedpoints.append(idnum)

# Log exisiting point shapefiles
fileopen = open("{}\\alreadyrun.txt".format(intermediateFolder), "w")
for filename in finishedpoints:
    fileopen.write('\n{}'.format(filename))
fileopen.close()

# look at images not represented in exisiting point shapefiles
for filename2 in os.listdir(imageFolder):
    y = filename2[-3] + filename2[-2] + filename2[-1]
    if y == 'tif' and filename2[:8] not in finishedpoints:

        largefilelist.append(filename2)

# log images not represented in exisiting point shapefiles
fileopen = open("{}\\torunstill.txt".format(intermediateFolder), "w")
for filename in largefilelist:
    fileopen.write('\n{}'.format(filename))
fileopen.close()
print("marker1")
print(largefilelist)
for filename in largefilelist:
    print (datetime.datetime.now())
    torunlist = []
    sectionid = filename[0:2]
    sectionid = sectionid + filename[3:5]
    sectionid = sectionid + filename[6:8]

    for row in cursor:
        needtoadd = 0
        rowval = str(row[1])
        tablesectid = str(rowval[1:7])
        if sectionid == tablesectid:
            print ('found a flight point')
            if len(torunlist) == 0:
                needtoadd = (row[2], str(row[0]))
            else:
                foundsimilar = 0
                for angle, direction in torunlist:
                    if (abs(row[2] - angle)) < angleDiff and direction == row[0]:
                        foundsimilar = 1
                if foundsimilar == 0:
                    needtoadd = (row[2], str(row[0]))
            if needtoadd != 0:
                torunlist.append(needtoadd)
                print ('appended', needtoadd)

    cursor.reset()
    print ('torunlist=', torunlist)
    print ('filename=', filename)

    if len(torunlist) == 0:
        print 'nothing in torunlist , moving on...'

    for diffpoint in torunlist:
        buildkernal(diffpoint[0], intermediateFolder, shadowwidth, shadowlength)

        # Script arguments
        print('step0.1')

        # Local variables:
        
        #ct_reclas_4 = "{}\\ct_reclas_4".format(mypath)
        #findSWall_5 = "{}\\findSWall_5".format(mypath)
        # scaledpts_7 = "{}\\scaledpts_7".format(mypath)
        # allones_8 = "{}\\allones_8".format(mypath)
        # valbelow70_9 = "{}\\valbelow70_9".format(mypath)
        # shadregions = "{}\\shadregions".format(mypath)
        # apply10 = "{}\\apply10".format(mypath)
        # onlyones = "{}\\onlyones".format(mypath)
        # morethanone = "{}\\morethanone".format(mypath)
        # morewvalue_11 = "{}\\morewvalue_11".format(mypath)
        # shiftcla_12 = "{}\\shiftcla_12".format(mypath)
        # claval_13 = "{}\\claval_13".format(mypath)
        # clatoshad_14 = "{}\\clatoshad_14".format(mypath)
        # finalrast_28 = "{}\\finalrast_28".format(mypath)
        # 
        # mineuclid = "{}\\mineuclid".format(mypath)
        # onlyswleft_15 = "{}\\onlyswleft_15".format(mypath)
        #reunite_16 = "{}\\reunite_16".format(mypath)
        #missedpts_17 = "{}\\missedpts_17".format(mypath)
        #maxzone_3 = "{}\\maxzone_3".format(mypath)
        #addmissed_18 = "{}\\addmissed_18".format(mypath)
        #shifted32 = "{}\\shifted32".format(mypath)
        #shadmask2_19 = "{}\\shadmask2_19".format(mypath)
        #shdmskreg_19 = "{}\\shdmskreg_19".format(mypath)
        #ptswsrval_20 = "{}\\ptswsrval_20".format(mypath)
        #ptswsrval_20__2_ = ptswsrval_20
        #morethanone21 = "{}\\morethanone21".format(mypath)
        #mrewthval_22 = "{}\\mrewthval_22".format(mypath)
        #mrewthval_22__2_ = mrewthval_22
        #mineuclidtwo = "{}\\mineuclidtwo".format(mypath)
        #swleft_25 = "{}\\swleft_25".format(mypath)
        #onlyones2 = "{}\\onlyones2".format(mypath)
        #onlyswleft_26 = "{}\\onlyswleft_26".format(mypath)
        #finalrast_27 = "{}\\finalrast_27".format(mypath)
        #polyptsmask3_shp = "{}\\polyptsmask3.shp".format(mypath)

        finalrast_29 = os.path.join(intermediateFolder,"finalrast_29")
        #binbin = os.path.join(intermediateFolder, "binbin")
        onlyones2p = os.path.join(intermediateFolder,"onlyones2p")
        onlysel_Merge = os.path.join(intermediateFolder,"onlysel_Merge")
        oyswleft_27 = os.path.join(intermediateFolder,"oyswleft_27")
        swleft_25p = os.path.join(intermediateFolder,"swleft_25p")

        txtnumst = str(diffpoint[0])
        dirst = str(diffpoint[1])

        filenamec = Raster('{0}\\{1}\\Band_1'.format(imageFolder, filename))
        township = sectionid[:2]
        rrange = sectionid[2:4]
        section = sectionid[4:6]

        print('step0.3')
        trsraster = "{}\\trsraster".format(intermediateFolder)

        # Process: Feature Class to Feature Class
        arcpy.FeatureClassToFeatureClass_conversion(trsfile, intermediateFolder, "current8.shp",
                                                    "\"TOWNSHIP\" = '{0}03' AND \"RANGE\" = '{1}02' AND \"SECTION\" = '{2}'".format(
                                                        township, rrange, section),
                                                    "FID_1 \"FID_1\" true true false 10 Long 0 10 ,First,#,trs,FID_1,-1,-1;TOWNSHIP \"TOWNSHIP\" true true false 4 Text 0 0 ,First,#,trs,TOWNSHIP,-1,-1;RANGE \"RANGE\" true true false 4 Text 0 0 ,First,#,trs,RANGE,-1,-1;SECTION \"SECTION\" true true false 2 Text 0 0 ,First,#,trs,SECTION,-1,-1;Count_ \"Count_\" true true false 10 Long 0 10 ,First,#,trs,Count_,-1,-1;Sum_GRID_C \"Sum_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Sum_GRID_C,-1,-1;Avg_GRID_C \"Avg_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Avg_GRID_C,-1,-1;Min_GRID_C \"Min_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Min_GRID_C,-1,-1;Max_GRID_C \"Max_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Max_GRID_C,-1,-1;Var_GRID_C \"Var_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Var_GRID_C,-1,-1;SD_GRID_CO \"SD_GRID_CO\" true true false 19 Double 0 0 ,First,#,trs,SD_GRID_CO,-1,-1;Sum_RASTER \"Sum_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Sum_RASTER,-1,-1;Avg_RASTER \"Avg_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Avg_RASTER,-1,-1;Min_RASTER \"Min_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Min_RASTER,-1,-1;Max_RASTER \"Max_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Max_RASTER,-1,-1;Var_RASTER \"Var_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Var_RASTER,-1,-1;SD_RASTERV \"SD_RASTERV\" true true false 19 Double 0 0 ,First,#,trs,SD_RASTERV,-1,-1;Area \"Area\" true true false 13 Float 0 0 ,First,#,trs,Area,-1,-1;Density \"Density\" true true false 13 Float 0 0 ,First,#,trs,Density,-1,-1",
                                                    "")
        print('step0.35')
        onepoly = "{}\\current8.shp".format(intermediateFolder)
        extent = arcpy.Describe(onepoly).extent
        west = extent.XMin
        south = extent.YMin
        east = extent.XMax
        north = extent.YMax
        # Process: Clip
        arcpy.Clip_management(filenamec,
                              "{0} {1} {2} {3}".format(west - 10, south, east + 10, north), trsraster,
                              onepoly, "256", "NONE", "NO_MAINTAIN_EXTENT")
        print('step0.36')
        # Local variables:
        filenamec = Raster(trsraster)

        print ('started ', filename)
        # Process: Focal Statistics

        print 'step1 - Summing shadow pixels'
        shadow_mean = arcpy.sa.FocalStatistics(filenamec,
                                    "Irregular {0}\\customk{1}.txt".format(intermediateFolder, diffpoint[1]), "MEAN",
                                    "DATA")
        print 'step2 - Summing below shadow pixels'
        # Process: Focal Statistics (3)
        above_mean = arcpy.sa.FocalStatistics(filenamec,
                                    "Irregular {0}\\customkabove{1}.txt".format(intermediateFolder, diffpoint[1]),
                                    "MEAN", "DATA")
        print 'step3 - Summing above shadow pixels'
        # Process: Focal Statistics (2)
        below_mean = arcpy.sa.FocalStatistics(filenamec,
                                    "Irregular {0}\\customkbelow{1}.txt".format(intermediateFolder, diffpoint[1]),
                                    "MEAN", "DATA")
        shad_ratio44 = (above_mean + below_mean) / shadow_mean
        shad_ratio66 = (above_mean + below_mean) / shadow_mean

        try:
            shad_ratio44.save(os.getcwd())
            print("saving passed!")
        except:
            print("saving failed!")
        shad_ratio55=shad_ratio44
        shad_ratio77 = (above_mean + below_mean) / shadow_mean

        print 'step4 - Discarding values below 4'
        # Process: Reclassify
   
        morethan43_1 = Con(shad_ratio77 >= 5, 1)

        print 'step 5 - Grouping regions'
        # Process: Region Group
        
        region_cro_2 = arcpy.sa.RegionGroup(morethan43_1, "EIGHT", "WITHIN", "NO_LINK", "")

        print 'step 6 - Taking the max of zones'
        # Process: Calculate max
        maxzone_3 = arcpy.sa.ZonalStatistics(region_cro_2, "VALUE", shad_ratio44, "MAXIMUM", "DATA")

        print 'step 7 - Counting number of pixels in zones'
        # Process: Reclassify (2)
        ct_reclas_4 = arcpy.sa.Reclassify(region_cro_2, "COUNT",
                               "0.500000 1.500000 1;1.500000 2.500000 2;2.500000 3.500000 3;3.500000 900 4",
                               "NODATA")

        print 'step 8 - Finding pixels closest to sun'
        # Process: Focal Statistics (7)
        findSWall_5 = arcpy.sa.FocalStatistics(ct_reclas_4,
                                    "Weight {0}\\s{1}.txt".format(intermediateFolder, diffpoint[1]),
                                    "SUM", "DATA")
        print 'step 9 - Deleteing pixels furthest from sun'
        # Process: Reclassify (3)

        scaledpts_7 = Con(((findSWall_5) == 9) | ((findSWall_5) == 18) | ((findSWall_5) == 27) | ((findSWall_5) == 36), 1)
        print 'step 10 - Shifting into shadow region'
        # Process: Focal Statistics (4)
        allones_8 = arcpy.sa.FocalStatistics(scaledpts_7,
                                    "Weight {0}\\shiftback{1}.txt".format(intermediateFolder, diffpoint[1]), "SUM",
                                    "DATA")
        print 'step 11 - Calculating shadow areas'
        # Process: Reclassify (4)
        valbelow70_9 = Con(filenamec <=70, 1)

        print 'step 12 - Grouping shadow areas into regions'
        # Process: Region Group (3)
        shadregions = arcpy.sa.RegionGroup(valbelow70_9, "EIGHT", "WITHIN", "NO_LINK", "")
        print 'step 13 - Writing shadow region values to shifted pixels'
        # Process: Raster Calculator (3)
        apply10 = Con(allones_8 > 0, shadregions)
        apply10.save('{}\\apply10'.format(intermediateFolder))
        print 'step 14 - Building attribute table'
        # Process: Build Raster Attribute Table (2)
        arcpy.BuildRasterAttributeTable_management(apply10, "Overwrite")
        print 'step 15 - Writing shadow region values to shifted pixels'
        # Process: Reclassify (7)
        onlyones = arcpy.sa.Reclassify(apply10, "Count", "1 1",  "NODATA")
        print 'step 16 - Finding duplicates within a shadow region'

        morethanone=arcpy.sa.Reclassify(apply10, "Count", "1.500000 30 1",  "NODATA")
        print 'step 17 - Writing shadow region values to shifted pixels'

        morewvalue_11 = Con(morethanone > 0, apply10)
        morewvalue_11.save('{}\\morewvalue_11'.format(intermediateFolder))

        # Process: Build Raster Attribute Table (3)
        arcpy.BuildRasterAttributeTable_management(morewvalue_11, "Overwrite")
        print 'step 18 Shift the original region count '

        # Process: Focal Statistics (6)
        shiftcla_12 = arcpy.sa.FocalStatistics(ct_reclas_4,
                                    "Weight {0}\\shiftback{1}.txt".format(intermediateFolder, diffpoint[1]), "SUM",
                                    "DATA")

        if morewvalue_11.mean == None or morewvalue_11.mean == 0:
            print 'no sags, moving on...'
            fileopen = open("{}\\nosags.txt".format(finishedFolder), "a")
            fileopen.write('\n{}'.format(filename))
            fileopen.close()

        else:
            # Process: Zonal Statistics (3)
            claval_13 = arcpy.sa.ZonalStatistics(morewvalue_11, "Value", shiftcla_12,  "MAXIMUM", "DATA")
            print 'step 19 Give all cells in shadow region maximum count '

            clatoshad_14 = (Con(claval_13 == shiftcla_12, apply10))
            clatoshad_14.save('{}\\clatoshad_14'.format(intermediateFolder))
            print 'step20'
            # Process: Build Raster Attribute Table (5)
            arcpy.BuildRasterAttributeTable_management(clatoshad_14, "Overwrite")
            print 'step21'
            newdistfile = finddist(clatoshad_14, diffpoint[1], intermediateFolder)
            print 'step22'
            # Process: Zonal Statistics
            mineuclid = arcpy.sa.ZonalStatistics(clatoshad_14, "Value", newdistfile,  "MINIMUM", "DATA")
            print 'step23'

            onlyswleft_15 = Con(mineuclid == newdistfile, 1)
            onlyswleft_15.save('{}\\onlyswleft_15'.format(intermediateFolder))
            print 'step24'

            reunite_16 = Con(IsNull(onlyones), onlyswleft_15, onlyones)
            reunite_16.save('{}\\reunite_16'.format(intermediateFolder))
            print 'step25'

            missedpts_17 = Con((allones_8 > 0) & (IsNull(shadregions)), 1)
            missedpts_17.save('{}\\missedpts_17'.format(intermediateFolder))

            print 'step26'
            addmissed_18 = Con(IsNull(reunite_16), missedpts_17, reunite_16)
            addmissed_18.save('{}\\addmissed_18'.format(intermediateFolder))

            if addmissed_18.extent.width <= 0.5:
                print 'no sags, moving on...'
                fileopen = open("{}\\nosags.txt".format(finishedFolder), "a")
                fileopen.write('\n{}'.format(filename))
                fileopen.close()

            else:
                print 'step27'
                # Process: Focal Statistics (5)
                shifted32 = arcpy.sa.FocalStatistics(addmissed_18,
                                            "Weight {0}\\shifttoshad{1}.txt".format(intermediateFolder, diffpoint[1]),
                                            "SUM", "DATA")
                check2 = shifted32
                print 'step28'
                if check2.mean == 0 or check2.mean == None:
                    print 'no sags, moving on...'
                    fileopen = open("{}\\nosags.txt".format(finishedFolder), "a")
                    fileopen.write('\n{}'.format(filename))
                    fileopen.close()
                else:
                    # Process: Reclassify (5)
                    shadmask2_19 = arcpy.sa.Reclassify(shad_ratio44, "VALUE", "0 2.290000 NODATA;2.290000 100 1",
                                           "NODATA")
                    print 'step28'
                    # Process: Region Group (2)
                    shdmskreg_19 = arcpy.sa.RegionGroup(shadmask2_19,  "EIGHT", "WITHIN", "NO_LINK", "")
                    print 'step29'

                    ptswsrval_20 = Con(shifted32 > 0, shdmskreg_19, )

                    ptswsrval_20.save('{}\\ptswsrval_20'.format(intermediateFolder))
                    print 'step30'
                    # Process: Build Raster Attribute Table
                    print 'step31'
                    arcpy.BuildRasterAttributeTable_management(ptswsrval_20, "Overwrite")
                    print 'step32'
                    # Process: Reclassify (10)
                    morethanone21 = arcpy.sa.Reclassify(ptswsrval_20, "Count", "1.500000 100 1",  "NODATA")

                    mrewthval_22 = Con('morethanone21' > 0, ptswsrval_20)
                    mrewthval_22.save('{}\\mrewthval_22'.format(intermediateFolder))

                    print 'step33'
                    # Process: Build Raster Attribute Table (4)
                    arcpy.BuildRasterAttributeTable_management(mrewthval_22, "NONE")
                    print 'step34'
                    # Process: Zonal Statistics (2)
                    if mrewthval_22.mean == 0:
                        swleft_25 = mrewthval_22
                    else:
                        distfile23 = finddist(mrewthval_22, diffpoint[1], intermediateFolder)

                        mineuclidtwo=arcpy.sa.ZonalStatistics(mrewthval_22, "VALUE", distfile23, "MINIMUM", "DATA")

                        print 'step35'
                        swleft_25 = Con(mineuclidtwo == distfile23, mineuclidtwo)

                    swleft_25.save('{}\\swleft_25'.format(intermediateFolder))
                    print 'step36'
                    # Process: Reclassify (9)
                    onlyones2=arcpy.sa.Reclassify(ptswsrval_20, "Count", "1 1",  "NODATA")
                    print 'step37'

                    print 'step38'
                    if swleft_25.mean == 0 or swleft_25.mean == None:
                        finalrast_28 = Con(onlyones2 >= 0, maxzone_3)

                    else:
                        arcpy.RasterToPoint_conversion(onlyones2, onlyones2p, "VALUE")

                        # Process: Raster to Point (2)
                        arcpy.RasterToPoint_conversion(swleft_25, swleft_25p, "Value")

                        # Process: Merge
                        arcpy.Merge_management("{0}.shp;{1}.shp".format(onlyones2p, swleft_25p), onlysel_Merge,
                                               "POINTID \"POINTID\" true true false 0 Long 0 0 ,First,#,C:\\Users\\fcarter\\Documents\\ArcGIS\\Default.gdb\\onlyones2p,POINTID,-1,-1,C:\\Users\\fcarter\\Documents\\ArcGIS\\Default.gdb\\swleft_25p,POINTID,-1,-1;GRID_CODE \"GRID_CODE\" true true false 0 Long 0 0 ,First,#,C:\\Users\\fcarter\\Documents\\ArcGIS\\Default.gdb\\onlyones2p,GRID_CODE,-1,-1,C:\\Users\\fcarter\\Documents\\ArcGIS\\Default.gdb\\swleft_25p,GRID_CODE,-1,-1")

                        # Process: Point to Raster
                        arcpy.PointToRaster_conversion("{}.shp".format(onlysel_Merge), "FID", oyswleft_27,
                                                       "MOST_FREQUENT", "NONE", "0.5")
                        finalrast_28 = Con(Raster(oyswleft_27) >= 0, maxzone_3)
                    print 'step39'

                    print 'step40'
                    # Process: Assign ratio values to saguaro locations

                    finalrast_28.save("{}\\finalrast_28".format(intermediateFolder))
                    print 'step41'
                    # Process: Raster to Point (3)
                    arcpy.Clip_management(finalrast_28,
                                          "{0} {1} {2} {3}".format(west, south, east, north), finalrast_29,
                                          onepoly, "256", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

                    oldname = "s1{0}{2}{1}.shp".format(str(filename), txtnumst, dirst)
                    newname = "{0}{1}{2}{3}{4}Y".format(oldname[2:4], oldname[5:7], oldname[8:10], oldname[21],
                                                        oldname[23:-4])
                    newname2 = newname.replace(".", "_")
                    print('newname2 is {}'.format(newname2))

                    check1 = Raster(finalrast_29)
                    if check1.mean == 0 or check1.mean == None:
                        print 'no sags, moving on...'
                        fileopen = open("{}\\nosags.txt".format(finishedFolder), "a")
                        fileopen.write('\n{}'.format(filename))
                        fileopen.close()
                    else:

                        arcpy.RasterToPoint_conversion(finalrast_29,
                                                       "{0}\\{1}".format(finishedFolder, newname2),
                                                       "Value")
                        arcpy.gp.ExtractValuesToPoints_sa("{0}\\{1}{2}".format(finishedFolder, newname2,".shp"), dem, pointsWithElevation, "NONE",
                                                          "VALUE_ONLY")
                        final_points = os.path.join(finishedFolder, newname2)
                        arcpy.Select_analysis(pointsWithElevation, final_points, "\"RASTERVALU\" <{0}".format(maxelev))

#Part 3

#Part 4

# Process: Extract Values to Points
#arcpy.gp.ExtractValuesToPoints_sa(saguarosPoints, dem, pointsWithElevation, "NONE", "VALUE_ONLY")
#arcpy.Select_analysis(pointsWithElevation, delpts, "\"RASTERVALU\" <{0}".format(maxelev))

print ("finished")