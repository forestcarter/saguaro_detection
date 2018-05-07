import arcpy
import os

saguarosPoints = arcpy.GetParameterAsText(0).replace("/", "//")
dem = arcpy.GetParameterAsText(1).replace("/", "//")
maxelev= arcpy.GetParameterAsText(2).replace("/", "//")
pointsWithElevation = arcpy.GetParameterAsText(3).replace("/", "//")
delpts= arcpy.GetParameterAsText(4).replace("/", "//")


# Process: Extract Values to Points
arcpy.gp.ExtractValuesToPoints_sa(saguarosPoints, dem, pointsWithElevation, "NONE", "VALUE_ONLY")


arcpy.Select_analysis(pointsWithElevation, delpts, "\"RASTERVALU\" <{0}".format(maxelev))





