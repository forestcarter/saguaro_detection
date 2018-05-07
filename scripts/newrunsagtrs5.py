import os
import math
import arcpy
from arcpy.sa import *
import datetime
arcpy.CheckOutExtension('Spatial')
localpath="C:\\Users\\fcarter\\Desktop\\localtext"
laptop=False
driveletter = "D"
if laptop == True:
    localpath = "C:\\Users\\forest\\Desktop\\localtext"
    driveletter = "E"
masterpath="{}:\\master".format(driveletter)
myfolder="snpsagout8"
mypath = "{0}\\{1}".format(masterpath,myfolder)
mypath2 = "{0}\\finished2".format(masterpath)

localmachine=False
if localmachine==True:
    masterpath="C:\\Users\\fcarter\\Desktop\\master"
    mypath = "{0}\\{1}".format(masterpath,myfolder)
    mypath2 = "{0}\\finished".format(masterpath)

if os.path.isdir(mypath):
    os.system('rmdir {} /s /q'.format(mypath))
    os.system('mkdir {}'.format(mypath)) 
    os.system('mkdir {}\\binbin'.format(mypath))
    pass

else:
    os.system('mkdir {}'.format(mypath))
    #os.system('mkdir {}'.format(mypath2))
    os.system('mkdir {}\\binbin'.format(mypath))


os.chdir(mypath)
arcpy.env.scratchWorkspace = mypath
arcpy.env.workspace = mypath
arcpy.env.overwriteOutput = True



print 'begin'
# Begin Kernal function
def buildkernal(rawangle, mypath):
    os.chdir(mypath)
    kernalcomplete = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

    shiftfactor = 4
    width = 2.0
    halfwidth = width / 2
    # The length was 8, lets try ten
    length = 10
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
    kernalcomplete = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    kernalcomplete = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        os.chdir(mypath)

        # flip shadshift
        f = open("{}\\shifttoshadw.txt".format(mypath), "w")
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


        #numpy.savetxt("{}\\shifttoshadw2.txt".format(mypath), masterlist )

        # flip shiftback
        f = open("{}\\shiftbackw.txt".format(mypath), "w")
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
        f = open("{}\\customkw.txt".format(mypath), "w")
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
        f = open("{}\\customkabovew.txt".format(mypath), "w")
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
        f = open("{}\\customkbeloww.txt".format(mypath), "w")
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
    path2=path+"\\binbin"
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


cursor = arcpy.da.SearchCursor('{}\\flightpoints\\joined\\fp_trs.shp'.format(masterpath), ["eastwest", "TILE_NAME", 'az2'])

cursor.reset()
print 'begin2'

# look at exisiting point shapefiles
largefilelist = []
finishedpoints = []
for filename3 in (os.listdir(mypath2)):
    idnum="{}S{}E{}".format(filename3[0:2],filename3[2:4],filename3[4:6])
    finishedpoints.append(idnum)
    
# Log exisiting point shapefiles
fileopen = open("{}\\alreadyrun.txt".format(mypath), "w")
for filename in finishedpoints:
    fileopen.write('\n{}'.format(filename))
fileopen.close()

# look at images not represented in exisiting point shapefiles
for filename2 in os.listdir('{}\\PAG_2011_6inchOrtho'.format(masterpath)):
    y = filename2[-3] + filename2[-2] + filename2[-1]
    if y == 'tif' and filename2[:8] not in finishedpoints:
        #Next line for specific file
        #if filename2[:8]=="15S17E14":
        largefilelist.append(filename2)
        
# log images not represented in exisiting point shapefiles
fileopen = open("{}\\torunstill.txt".format(mypath), "w")
for filename in largefilelist:
    fileopen.write('\n{}'.format(filename))
fileopen.close()



for filename in largefilelist:
    
    print (datetime.datetime.now())

    torunlist = []
    sectionid = filename[0:2]
    sectionid = sectionid + filename[3:5]
    sectionid = sectionid + filename[6:8]

    # get east/west and textfilenumber
    # torunlist is a list of tuples with (az3, eorw)

    for row in cursor:


        needtoadd = 0
        rowval = row[1]
        tablesectid = rowval[1:7]
        if sectionid == tablesectid:
            print ('found a flight point')
            if len(torunlist) == 0:
                needtoadd = (row[2], str(row[0]))

                # fileopen2 = open("F:\\result.txt", "a")
                # fileopen2.write('added first fp {}\n'.format(str(needtoadd)))
                # fileopen2.close()
            else:
                foundsimilar = 0
                for angle, direction in torunlist:
                    if (abs(row[2] - angle)) < 10 and direction == row[0]:
                        foundsimilar = 1

                if foundsimilar == 0:
                    needtoadd = (row[2], str(row[0]))
                    # fileopen2 = open("F:\\result.txt", "a")
                    # fileopen2.write('added additional fp {}\n'.format(str(needtoadd)))
                    # fileopen2.close()

            if needtoadd != 0:
                torunlist.append(needtoadd)
                print ('appended', needtoadd)

    cursor.reset()
    print ('torunlist=', torunlist)
    print ('filename=', filename)

    #Assign angle to section with no flightpoint
    # if filename=='15S16E05_C50Y11.tif':
    #     print 'found no flight point 151605'
    #     torunlist.append((-74.3164, 'e'))

    if len(torunlist)==0:
        print 'nothing in torunlist , moving on...'

    for diffpoint in torunlist:
        buildkernal(diffpoint[0], mypath)

        # Script arguments
        print('step0.1')
        SNPBoundaries = arcpy.GetParameterAsText(0)
        if SNPBoundaries == '#' or not SNPBoundaries:
            SNPBoundaries = "SNPBoundaries"  # provide a default value if unspecified

        v14S16E17_C50Y11_tif = arcpy.GetParameterAsText(1)
        if v14S16E17_C50Y11_tif == '#' or not v14S16E17_C50Y11_tif:
            v14S16E17_C50Y11_tif = "14S16E17_C50Y11.tif"  # provide a default value if unspecified

        snpeuclidsw__2_ = arcpy.GetParameterAsText(2)
        if snpeuclidsw__2_ == '#' or not snpeuclidsw__2_:
            snpeuclidsw__2_ = "snpeuclidsw"  # provide a default value if unspecified

        v14S16E17_C50Y11_tif__2_ = arcpy.GetParameterAsText(3)
        if v14S16E17_C50Y11_tif__2_ == '#' or not v14S16E17_C50Y11_tif__2_:
            v14S16E17_C50Y11_tif__2_ = "14S16E17_C50Y11.tif"  # provide a default value if unspecified
        print('step0.2')
        # Local variables:
        cliptosnp = "{}\\cliptosnp".format(mypath)
        above_mean = "{}\\above_mean".format(mypath)
        below_mean = "{}\\below_mean".format(mypath)
        shadow_mean = "{}\\shadow_mean".format(mypath)
        shad_ratio = "{}\\shad_ratio".format(mypath)
        morethan43_1 = "{}\\morethan43_1".format(mypath)
        region_cro_2 = "{}\\region_cro_2".format(mypath)
        ct_reclas_4 = "{}\\ct_reclas_4".format(mypath)
        findSWall_5 = "{}\\findSWall_5".format(mypath)
        scaledpts_7 = "{}\\scaledpts_7".format(mypath)
        shift2shad = "{}\\shift2shad".format(mypath)
        allones_8 = "{}\\allones_8".format(mypath)
        valbelow70_9 = "{}\\valbelow70_9".format(mypath)
        shadregions = "{}\\shadregions".format(mypath)
        apply10 = "{}\\apply10".format(mypath)
        onlyones = "{}\\onlyones".format(mypath)
        morethanone = "{}\\morethanone".format(mypath)
        morewvalue_11 = "{}\\morewvalue_11".format(mypath)
        shiftcla_12 = "{}\\shiftcla_12".format(mypath)
        claval_13 = "{}\\claval_13".format(mypath)
        clatoshad_14 = "{}\\clatoshad_14".format(mypath)
        finalrast_28 = "{}\\finalrast_28".format(mypath)
        finalrast_29 = "{}\\finalrast_29".format(mypath)
        mineuclid = "{}\\mineuclid".format(mypath)
        onlyswleft_15 = "{}\\onlyswleft_15".format(mypath)
        reunite_16 = "{}\\reunite_16".format(mypath)
        missedpts_17 = "{}\\missedpts_17".format(mypath)
        maxzone_3 = "{}\\maxzone_3".format(mypath)
        addmissed_18 = "{}\\addmissed_18".format(mypath)
        shifted32 = "{}\\shifted32".format(mypath)
        shadmask2_19 = "{}\\shadmask2_19".format(mypath)
        shdmskreg_19 = "{}\\shdmskreg_19".format(mypath)
        ptswsrval_20 = "{}\\ptswsrval_20".format(mypath)
        ptswsrval_20__2_ = ptswsrval_20
        morethanone21 = "{}\\morethanone21".format(mypath)
        mrewthval_22 = "{}\\mrewthval_22".format(mypath)
        mrewthval_22__2_ = mrewthval_22
        mineuclidtwo = "{}\\mineuclidtwo".format(mypath)
        swleft_25 = "{}\\swleft_25".format(mypath)
        onlyones2 = "{}\\onlyones2".format(mypath)
        onlyswleft_26 = "{}\\onlyswleft_26".format(mypath)
        finalrast_27 = "{}\\finalrast_27".format(mypath)
        polyptsmask3_shp = "{}\\polyptsmask3.shp".format(mypath)
        trs = "{}\\trsfile\\trs.shp".format(masterpath)
        binbin = "{}\\binbin".format(mypath)
        maxsr_24 = "{}\\maxsr_24".format(mypath)
        maxzone_32 = "{}\\onlyones2p".format(mypath)
        onlyones2p = "{}\\onlyones2p".format(mypath)
        swleft_25p = "{}\\swleft_25p".format(mypath)
        onlysel_Merge = "{}\\onlysel_Merge".format(mypath)
        oyswleft_27 = "{}\\oyswleft_27".format(mypath)

        
        txtnumst = str(diffpoint[0])
        dirst = str(diffpoint[1])

        # Set Geoprocessing environments
        filenamec = Raster('{0}\\PAG_2011_6inchOrtho\\{1}\\Band_1'.format(masterpath, filename))

        #############################

        township = sectionid[:2]
        rrange = sectionid[2:4]
        section = sectionid[4:6]


        print('step0.3')
        trsraster = "{}\\trsraster".format(mypath)

        # Process: Feature Class to Feature Class
        arcpy.FeatureClassToFeatureClass_conversion(trs, binbin, "current8.shp",
                                                    "\"TOWNSHIP\" = '{0}03' AND \"RANGE\" = '{1}02' AND \"SECTION\" = '{2}'".format(
                                                        township, rrange, section),
                                                    "FID_1 \"FID_1\" true true false 10 Long 0 10 ,First,#,trs,FID_1,-1,-1;TOWNSHIP \"TOWNSHIP\" true true false 4 Text 0 0 ,First,#,trs,TOWNSHIP,-1,-1;RANGE \"RANGE\" true true false 4 Text 0 0 ,First,#,trs,RANGE,-1,-1;SECTION \"SECTION\" true true false 2 Text 0 0 ,First,#,trs,SECTION,-1,-1;Count_ \"Count_\" true true false 10 Long 0 10 ,First,#,trs,Count_,-1,-1;Sum_GRID_C \"Sum_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Sum_GRID_C,-1,-1;Avg_GRID_C \"Avg_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Avg_GRID_C,-1,-1;Min_GRID_C \"Min_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Min_GRID_C,-1,-1;Max_GRID_C \"Max_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Max_GRID_C,-1,-1;Var_GRID_C \"Var_GRID_C\" true true false 19 Double 0 0 ,First,#,trs,Var_GRID_C,-1,-1;SD_GRID_CO \"SD_GRID_CO\" true true false 19 Double 0 0 ,First,#,trs,SD_GRID_CO,-1,-1;Sum_RASTER \"Sum_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Sum_RASTER,-1,-1;Avg_RASTER \"Avg_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Avg_RASTER,-1,-1;Min_RASTER \"Min_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Min_RASTER,-1,-1;Max_RASTER \"Max_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Max_RASTER,-1,-1;Var_RASTER \"Var_RASTER\" true true false 19 Double 0 0 ,First,#,trs,Var_RASTER,-1,-1;SD_RASTERV \"SD_RASTERV\" true true false 19 Double 0 0 ,First,#,trs,SD_RASTERV,-1,-1;Area \"Area\" true true false 13 Float 0 0 ,First,#,trs,Area,-1,-1;Density \"Density\" true true false 13 Float 0 0 ,First,#,trs,Density,-1,-1",
                                                    "")
        print('step0.35')
        onepoly = "{}\\binbin\\current8.shp".format(mypath)
        extent = arcpy.Describe(onepoly).extent
        west = extent.XMin
        south = extent.YMin
        east = extent.XMax
        north = extent.YMax
        # Process: Clip
        arcpy.Clip_management(filenamec,
                              "{0} {1} {2} {3}".format(west-10, south, east+10, north), trsraster,
                              onepoly, "256", "NONE", "NO_MAINTAIN_EXTENT")
        print('step0.36')
        # Local variables:
        filenamec=Raster(trsraster)

        print ('started ', filename)
        # Process: Focal Statistics



        print('step0.4')
        os.system('del {}\\*.txt /s /q'.format(localpath))
        print ('copy {0}\\*.txt {1}'.format(mypath,localpath))
        os.system('copy {0}\\*.txt {1}'.format(mypath,localpath))

        print 'step1 - Summing shadow pixels'
        arcpy.gp.FocalStatistics_sa(filenamec, shadow_mean,
                                    "Irregular {0}\\customk{1}.txt".format(localpath, diffpoint[1]), "MEAN", "DATA")
        print 'step2 - Summing below shadow pixels'
        # Process: Focal Statistics (3)
        arcpy.gp.FocalStatistics_sa(filenamec, above_mean,
                                    "Irregular {0}\\customkabove{1}.txt".format(localpath, diffpoint[1]), "MEAN", "DATA")
        print 'step3 - Summing above shadow pixels'
        # Process: Focal Statistics (2)
        arcpy.gp.FocalStatistics_sa(filenamec, below_mean,
                                    "Irregular {0}\\customkbelow{1}.txt".format(localpath, diffpoint[1]), "MEAN", "DATA")


        shad_ratio = (Raster('above_mean') + Raster('below_mean')) / Raster('shadow_mean')
        print (mypath)
        shad_ratio.save('{}\\shadratio'.format(mypath))

        print 'step4 - Discarding values below 4'

        # Process: Reclassify
        arcpy.gp.Reclassify_sa(shad_ratio, "VALUE", "0 5.0 NODATA; 5.0 100 1", morethan43_1, "NODATA")
        # arcpy.gp.Reclassify_sa(shad_ratio, "VALUE", "0 4.383010 NODATA;4.300000 100 1", morethan43_1, "NODATA")
        # 4.483010 Worked on first run, let try 4.6
        print 'step 5 - Grouping regions'
        # Process: Region Group
        arcpy.gp.RegionGroup_sa(morethan43_1, region_cro_2, "EIGHT", "WITHIN", "NO_LINK", "")

        print 'step 6 - Taking the max of zones'
        # Process: Calculate max
        arcpy.gp.ZonalStatistics_sa(region_cro_2, "VALUE", shad_ratio, maxzone_3, "MAXIMUM", "DATA")

        print 'step 7 - Counting number of pixels in zones'
        # Process: Reclassify (2)
        arcpy.gp.Reclassify_sa(region_cro_2, "COUNT",
                               "0.500000 1.500000 1;1.500000 2.500000 2;2.500000 3.500000 3;3.500000 900 4",
                               ct_reclas_4, "NODATA")
        print 'step 8 - Finding pixels closest to sun'
        # Process: Focal Statistics (7)
        arcpy.gp.FocalStatistics_sa(ct_reclas_4, findSWall_5, "Weight {0}\\s{1}.txt".format(localpath,diffpoint[1]),
                                    "SUM", "DATA")
        # arcpy.gp.FocalStatistics_sa(ct_reclas_4, findSWall_5, "Weight F:\\snpsainput\\sunangles\\S{}.txt".format(diffpoint[1]), "SUM", "DATA")
        print 'step 9 - Deleteing pixels furthest from sun'
        # Process: Reclassify (3)
        arcpy.gp.Reclassify_sa(findSWall_5, "Value",
                               "0 8.990000 NODATA;9 1;9.001000 17.990000 NODATA;18 1;18.001000 26.990000 NODATA;27 1;27.001000 35.990000 NODATA;36 1;36.010000 100 NODATA",
                               scaledpts_7, "NODATA")
        print 'step 10 - Shifting into shadow region'
        # Process: Focal Statistics (4)
        arcpy.gp.FocalStatistics_sa(scaledpts_7, allones_8,
                                    "Weight {0}\\shiftback{1}.txt".format(localpath,diffpoint[1]), "SUM", "DATA")
        print 'step 11 - Calculating shadow areas'
        # Process: Reclassify (4)
        arcpy.gp.Reclassify_sa(filenamec, "Value", "0 70 1;70 300 NODATA", valbelow70_9, "NODATA")
        print 'step 12 - Grouping shadow areas into regions'
        # Process: Region Group (3)
        arcpy.gp.RegionGroup_sa(valbelow70_9, shadregions, "EIGHT", "WITHIN", "NO_LINK", "")
        print 'step 13 - Writing shadow region values to shifted pixels'
        # Process: Raster Calculator (3)
        apply10 = (Con(Raster('allones_8') > 0, Raster('shadregions')))
        apply10.save('{}\\apply10'.format(mypath))
        print 'step 14 - Building attribute table'
        # Process: Build Raster Attribute Table (2)
        arcpy.BuildRasterAttributeTable_management(apply10, "Overwrite")
        print 'step 15 - Writing shadow region values to shifted pixels'
        # Process: Reclassify (7)
        arcpy.gp.Reclassify_sa(apply10, "Count", "1 1", onlyones, "NODATA")
        print 'step 16 - Finding duplicates within a shadow region'
        # Process: Reclassify (8)
        # arcpy.gp.Reclassify_sa(apply23_10__3_, "Count", "1.500000 30 1", morethanone, "NODATA")
        arcpy.gp.Reclassify_sa(apply10, "Count", "1.500000 30 1", morethanone, "NODATA")
        print 'step 17 - Writing shadow region values to shifted pixels'
        # Process: Raster Calculator (2)
        # arcpy.gp.RasterCalculator_sa("Con(\"%morethanone%\">0, \"%apply23_10%\")", morewvalue_11)
        morewvalue_11 = Con(Raster('morethanone') > 0, apply10)
        morewvalue_11.save('{}\\morewvalue_11'.format(mypath))
        
        # Process: Build Raster Attribute Table (3)
        arcpy.BuildRasterAttributeTable_management(morewvalue_11, "Overwrite")
        print 'step 18 Shift the original region count '

        # Process: Focal Statistics (6)
        arcpy.gp.FocalStatistics_sa(ct_reclas_4, shiftcla_12,
                                    "Weight {0}\\shiftback{1}.txt".format(localpath,diffpoint[1]), "SUM", "DATA")

        
        if morewvalue_11.mean == None or  morewvalue_11.mean == 0:
            print 'no sags, moving on...'
            fileopen = open("{}\\nosags.txt".format(masterpath), "a")
            fileopen.write('\n{}'.format(filename))
            fileopen.close()

        else:
            # Process: Zonal Statistics (3)
            arcpy.gp.ZonalStatistics_sa(morewvalue_11, "Value", shiftcla_12, claval_13, "MAXIMUM", "DATA")
            print 'step 19 Give all cells in shadow region maximum count '

            # Process: Raster Calculator (8)
            # arcpy.gp.RasterCalculator_sa("Con(\"%claval_13%\"==\"%shiftcla_12%\", \"%apply23_10%\")", clatoshad_14)
            clatoshad_14 = (Con(Raster('claval_13') == Raster('shiftcla_12'), apply10))
            clatoshad_14.save('{}\\clatoshad_14'.format(mypath))
            print 'step20'
            # Process: Build Raster Attribute Table (5)
            arcpy.BuildRasterAttributeTable_management(clatoshad_14, "Overwrite")
            print 'step21'
            # Process: Raster Calculator (11)
            # arcpy.gp.RasterCalculator_sa("Con(\"%14S16E17_C50Y11.tif (2)%\">0, \"%real{}%\")".format(diffpoint[1]), clippedeuclid)
            # clippedeuclid = (Con(filenamec > 0, "F:\\euclid\\real{}".format(diffpoint[1])))
            # print 'step58.5'
            # clippedeuclid.save('{}\\snpsagout5\\clippedeuclid'.format(masterpath))
            # print 'step59'
            newdistfile=finddist(clatoshad_14, diffpoint[1], mypath)
            print 'step22'
            # Process: Zonal Statistics
            arcpy.gp.ZonalStatistics_sa(clatoshad_14, "Value", newdistfile, mineuclid, "MINIMUM", "DATA")
            print 'step23'
            # Process: Raster Calculator (9)
            # arcpy.gp.RasterCalculator_sa("Con(\"%mineuclid%\"==\"%clippedeuclid%\", 1)", onlyswleft_15)
            onlyswleft_15 = Con(Raster('mineuclid') == newdistfile, 1)
            onlyswleft_15.save('{}\\onlyswleft_15'.format(mypath))
            print 'step24'
            # Process: Raster Calculator (12)
            # arcpy.gp.RasterCalculator_sa("Con(IsNull(\"%onlyones%\"), \"%onlyswleft_15%\", \"%onlyones%\")", reunite_16)
            reunite_16 = Con(IsNull(Raster('onlyones')), onlyswleft_15, Raster('onlyones'))
            reunite_16.save('{}\\reunite_16'.format(mypath))
            print 'step25'
            # Process: Raster Calculator (6)
            # arcpy.gp.RasterCalculator_sa("Con((\"%allones_8%\">0) & (IsNull(\"%shadregions%\")), 1)", missedpts_17)
            missedpts_17 = Con((Raster('allones_8') > 0) & (IsNull(Raster('shadregions'))), 1)
            missedpts_17.save('{}\\missedpts_17'.format(mypath))
            # Process: Raster Calculator (7)
            # arcpy.gp.RasterCalculator_sa("Con(IsNull(\"%reunite_16%\"), \"%missedpts_17%\", \"%reunite_16%\")", addmissed_18)
            print 'step26'
            addmissed_18 = Con(IsNull(reunite_16), missedpts_17, reunite_16)
            addmissed_18.save('{}\\addmissed_18'.format(mypath))
            
            if addmissed_18.extent.width<=0.5:
                print 'no sags, moving on...'
                fileopen = open("{}\\nosags.txt".format(masterpath), "a")
                fileopen.write('\n{}'.format(filename))
                fileopen.close()

            else:
                print 'step27'
                # Process: Focal Statistics (5)
                arcpy.gp.FocalStatistics_sa(addmissed_18, shifted32, "Weight {0}\\shifttoshad{1}.txt".format(localpath,diffpoint[1]),
                                            "SUM", "DATA")
                check2=Raster('shifted32')
                print 'step28'
                if check2.mean==0 or check2.mean==None:
                    print 'no sags, moving on...'
                    fileopen = open("{}\\nosags.txt".format(masterpath), "a")
                    fileopen.write('\n{}'.format(filename))
                    fileopen.close()
                else:
                    
                    # Process: Reclassify (5)
                    arcpy.gp.Reclassify_sa(shad_ratio, "VALUE", "0 2.290000 NODATA;2.290000 30 1", shadmask2_19, "NODATA")
                    print 'step28'
                    # Process: Region Group (2)
                    arcpy.gp.RegionGroup_sa(shadmask2_19, shdmskreg_19, "EIGHT", "WITHIN", "NO_LINK", "")
                    print 'step29'
                    # Process: Raster Calculator (4)
                    # arcpy.gp.RasterCalculator_sa("Con(\"%shifted32%\">0, \"%shdmskreg_19%\")", ptswsrval_20)
                    ptswsrval_20 = Con(Raster('shifted32') > 0, Raster('shdmskreg_19'), )
                    
                    ptswsrval_20.save('{}\\ptswsrval_20'.format(mypath))
                    print 'step30'
                    # Process: Build Raster Attribute Table
                    print 'step31'
                    arcpy.BuildRasterAttributeTable_management(ptswsrval_20, "Overwrite")
                    print 'step32'
                    # Process: Reclassify (10)
                    arcpy.gp.Reclassify_sa(ptswsrval_20, "Count", "1.500000 100 1", morethanone21, "NODATA")

                    # Process: Raster Calculator (14)
                    # arcpy.gp.RasterCalculator_sa("Con(\"%morethanone21%\">0,\"%ptswsrval_20%\")", mrewthval_22)
                    mrewthval_22 = Con(Raster('morethanone21') > 0, ptswsrval_20)
                    mrewthval_22.save('{}\\mrewthval_22'.format(mypath))

                    print 'step33'
                    # Process: Build Raster Attribute Table (4)
                    arcpy.BuildRasterAttributeTable_management(mrewthval_22, "NONE")
                    print 'step34'
                    # Process: Zonal Statistics (2)
                    if mrewthval_22.mean==0:
                        swleft_25 = Raster('mrewthval_22')
                    else:
                        distfile23 = finddist(mrewthval_22, diffpoint[1], mypath)

                        arcpy.gp.ZonalStatistics_sa(mrewthval_22, "VALUE", distfile23, mineuclidtwo, "MINIMUM", "DATA")
                        ###
                        # maxsr_24 = Con(Raster('mineuclidtwo') > 0, Raster('shadratio'))
                        # maxsr_24.save('{}\\snpsagout5\\maxsr_24'.format(masterpath))
                        # arcpy.gp.ZonalStatistics_sa(maxsr_24, "VALUE", shdmskreg_19, maxzone_32, "MAXIMUM", "DATA")
                        ###
                        print 'step35'
                        swleft_25 = Con(Raster('mineuclidtwo') == distfile23, Raster('mineuclidtwo'))
                    
                    swleft_25.save('{}\\swleft_25'.format(mypath))
                    print 'step36'
                    # Process: Reclassify (9)
                    arcpy.gp.Reclassify_sa(ptswsrval_20, "Count", "1 1", onlyones2, "NODATA")
                    print 'step37'
                    # Process: Raster Calculator (13)
                    # arcpy.gp.RasterCalculator_sa("Con(IsNull(\"%swleft%\"), \"%onlyones2%\", \"%swleft%\")", onlyswleft_26)
                    print 'step38'
                    if swleft_25.mean==0 or swleft_25.mean==None:
                        #oyswleft_27 = Raster('onlyones2')
                        finalrast_28 = Con(Raster('onlyones2') >= 0, maxzone_3)

                    else:
                        #oyswleft_27 = Con(IsNull(Raster('onlyones2')), swleft_25, Raster('onlyones2'))


                        arcpy.RasterToPoint_conversion(Raster('onlyones2'), onlyones2p, "VALUE")

                        # Process: Raster to Point (2)
                        arcpy.RasterToPoint_conversion(swleft_25, swleft_25p, "Value")

                        # Process: Merge
                        arcpy.Merge_management("{0}.shp;{1}.shp".format(onlyones2p,swleft_25p), onlysel_Merge, "POINTID \"POINTID\" true true false 0 Long 0 0 ,First,#,C:\\Users\\fcarter\\Documents\\ArcGIS\\Default.gdb\\onlyones2p,POINTID,-1,-1,C:\\Users\\fcarter\\Documents\\ArcGIS\\Default.gdb\\swleft_25p,POINTID,-1,-1;GRID_CODE \"GRID_CODE\" true true false 0 Long 0 0 ,First,#,C:\\Users\\fcarter\\Documents\\ArcGIS\\Default.gdb\\onlyones2p,GRID_CODE,-1,-1,C:\\Users\\fcarter\\Documents\\ArcGIS\\Default.gdb\\swleft_25p,GRID_CODE,-1,-1")

                        # Process: Point to Raster
                        arcpy.PointToRaster_conversion("{}.shp".format(onlysel_Merge), "FID", oyswleft_27, "MOST_FREQUENT", "NONE", "0.5")
                        finalrast_28 = Con(Raster(oyswleft_27) >= 0, maxzone_3)
                    #oyswleft_27.save('{}\\oyswleft_27'.format(mypath))
                    print 'step39'
                    # Process: Raster Calculator (5)
                    # arcpy.gp.RasterCalculator_sa("Con(IsNull(\"%shad_ratio%\"),\"%onlyswleft_26%\", Con(IsNull(\"%ct_reclas_4%\"),\"%onlyswleft_26%\", #Con((\"%shad_ratio%\">4.35)   |  (\"%ct_reclas_4%\">1.1),\"%onlyswleft_26%\")))", finalrast_27)
                    # finalrast_27 = Con(IsNull(shad_ratio), onlyswleft_26, Con(IsNull(Raster('ct_reclas_4')), onlyswleft_26, Con(
                    #     ((shad_ratio > 4.35) | (Raster('ct_reclas_4') > 1.1) | (Raster('onlyswleft_26') > 4.35)), onlyswleft_26)))
                    # finalrast_27.save('{}\\snpsagout5\\finalrast_27'.format(masterpath))
                    print 'step40'
                    # Process: Assign ratio values to saguaro locations

                    finalrast_28.save("{}\\finalrast_28".format(mypath))
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

                    check1=Raster('finalrast_29')
                    if check1.mean==0 or check1.mean==None:
                        print 'no sags, moving on...'
                        fileopen = open("{}\\nosags.txt".format(masterpath), "a")
                        fileopen.write('\n{}'.format(filename))
                        fileopen.close()
                    else:
                        arcpy.RasterToPoint_conversion(finalrast_29,
                                                       "{0}\\{1}".format(mypath2,newname2),
                                                       "Value")

                        # Local variables:
    ##                    finalfile="{0}\\{1}.shp".format(mypath,newname2)
    ##                    largedem = "{0}\\dem\\largedem".format(masterpath)
    ##                    tablefolder="{0}\\tablefolder".format(mypath)
    ##                    sampletable="{0}\\st{1}".format(tablefolder,newname2)
    ##                    fieldname="F{}".format(newname2[0:15])
    ##                    print 'step42'
    ##
    ##                    # Process: Sample
    ##                    if os.path.isdir(tablefolder):
    ##                        # os.system('rmdir {} /s /q'.format(tablefolder))
    ##                        # print('deleted old table')
    ##                        pass
    ##                    else:
    ##                        os.system('mkdir {}'.format(tablefolder))
    ##            
    ##                    
    ##                    arcpy.gp.Sample_sa(largedem, finalfile, sampletable, "NEAREST", "FID", "CURRENT_SLICE")
    ##                    print 'step43'
    ##                    
    ##                    arcpy.MakeFeatureLayer_management(finalfile, "L{}".format(newname2))
    ##                    namedfield = arcpy.ListFields(sampletable)
    ##                    myfieldname=str(namedfield[1].name)
    ##                    print('target field is ', fieldname)
    ##                    print(str(sampletable))
    ##                    arcpy.AddJoin_management("L{}".format(newname2), "FID", sampletable, "{}".format(fieldname))
    ##                    print 'step44'
    ##                    arcpy.FeatureClassToFeatureClass_conversion("L{}".format(newname2), mypath2, fieldname)

        print (datetime.datetime.now())
