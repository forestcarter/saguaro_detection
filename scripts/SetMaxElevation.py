import arcpy
import os

pointsWithElevation = arcpy.GetParameterAsText(0)
maxElevation = arcpy.GetParameterAsText(1)
delete_elevation = arcpy.GetParameterAsText(2)

# Process: Extract Values to Points
arcpy.SelectLayerByAttribute_management(pointsWithElevation, "NEW_SELECTION", "\"RASTERVALU\"<{0}".format(maxElevation))

# Process: Copy Features
arcpy.CopyFeatures_management(pointsWithElevation, delete_elevation, "", "0", "0", "0")




