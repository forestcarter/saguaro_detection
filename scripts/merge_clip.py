# Updated 5/24/18 A newer version may be available https://github.com/forestcarter/saguaro_detection
import os
import math
import arcpy
from arcpy.sa import *
import datetime
import Pysolar.solar
arcpy.env.overwriteOutput = True
# locallat=(32.287117)
# locallong=(360-111.166215)
# angleDiff=10
#abPath=(os.path.dirname(os.path.realpath(__file__)))[:-8]
abPath=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#Part 1
if arcpy.GetParameterAsText(0)=='':
    print('no params')
    # #abPath=os.path.join("f:"+os.sep,"saguaro_detection_git")
    # dem = os.path.join(abPath, "dem", "largedem")
    # flightpoints = os.path.join(abPath, "Ortho2011_FlightPoints", "Pima_Photos_2011.shp")
    # trsfile =  os.path.join(abPath, "township_range_az", "trs.shp")
    # imageFolder = os.path.join(abPath, "PAG_2011_6inchOrtho")
    # shadowwidth = 2
    # shadowlength = 10
    # maxelev = 1550
    # intermediateFolder = os.path.join(abPath, "outputs","intermediate")

    SNPBoundaries_shp = os.path.join(abPath, "snp_boundary", "SNPBoundaries.shp")
    finishedFolder = os.path.join(abPath, "outputs","finished")
    finalFolder = os.path.join(abPath, "outputs","finalproducts")
    merged_shp = os.path.join(abPath, "finalFolder", "merged.shp")
    merged_clipped = os.path.join(abpath, "finalFolder", "merged_clipped.shp")
else:
    # dem = arcpy.GetParameterAsText(0)
    # SNPBoundaries_shp = arcpy.GetParameterAsText(1)
    # flightpoints = arcpy.GetParameterAsText(2)
    # trsfile = arcpy.GetParameterAsText(3)
    # imageFolder = arcpy.GetParameterAsText(4)
    # shadowwidth = int(arcpy.GetParameterAsText(5))
    # shadowlength = int(arcpy.GetParameterAsText(6))
    # maxelev= arcpy.GetParameterAsText(7)
    # intermediateFolder = arcpy.GetParameterAsText(8)

    SNPBoundaries_shp = arcpy.GetParameterAsText(0)
    finishedFolder = arcpy.GetParameterAsText(1)
    merged_shp = arcpy.GetParameterAsText(2)
    merged_clipped = arcpy.GetParameterAsText(3)



filelist=""
for name in os.listdir(finishedFolder):
    if name[-4:]==".shp" and name[:2]!="fp":
        filelist+=";"+name

# Process: Merge
os.chdir(finishedFolder)

arcpy.Merge_management(filelist[1:], merged_shp, "")
# Process: Clip
arcpy.Clip_analysis(merged_shp, SNPBoundaries_shp, merged_clipped, "")
