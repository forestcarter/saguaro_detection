import arcpy
import os

finishedFolder = arcpy.GetParameterAsText(0)
SNPBoundaries_shp = arcpy.GetParameterAsText(1)
merged_shp = arcpy.GetParameterAsText(2)
output2 = arcpy.GetParameterAsText(3)

filelist=""
for name in os.listdir(finishedFolder):
    if name[-4:]==".shp":
        filelist+=";"+name
os.chdir(finishedFolder)
print(finishedFolder)

# Process: Merge
#arcpy.Merge_management("121126e22_0627994537Y;121125e32_0741996765Y", merged_shp, "pointid \"pointid\" true true false 10 Long 0 10 ,First,#,121126e22_0627994537Y,pointid,-1,-1,121125e32_0741996765Y,pointid,-1,-1;grid_code \"grid_code\" true true false 13 Float 0 0 ,First,#,121126e22_0627994537Y,grid_code,-1,-1,121125e32_0741996765Y,grid_code,-1,-1")
arcpy.Merge_management(filelist[1:], merged_shp, "")
# Process: Clip
arcpy.Clip_analysis(merged_shp, SNPBoundaries_shp, output2, "")

