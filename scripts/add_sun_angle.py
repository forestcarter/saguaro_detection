import arcpy
import Pysolar.solar
arcpy.env.overwriteOutput = True
flightpoints = arcpy.GetParameterAsText(0)
trs = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)




locallat=(32.287117)
locallong=(360-111.166215)
# Process: Spatial Join
arcpy.SpatialJoin_analysis(flightpoints, trs, output, "JOIN_ONE_TO_ONE", "KEEP_ALL", "Date_ \"Date_\" true true false 10 Long 0 10 ,First,#,{0},Date_,-1,-1;GPSTime \"GPSTime\" true true false 19 Double 0 0 ,First,#,{0},GPSTime,-1,-1;TOWNSHIP \"TOWNSHIP\" true true false 4 Text 0 0 ,First,#,{1},TOWNSHIP,-1,-1;RANGE \"RANGE\" true true false 4 Text 0 0 ,First,#,{1},RANGE,-1,-1;SECTION \"SECTION\" true true false 2 Text 0 0 ,First,#,{1},SECTION,-1,-1".format(flightpoints,trs), "INTERSECT", "", "")

#arcpy.SpatialJoin_analysis(flightpoints, trs, output, "JOIN_ONE_TO_ONE", "KEEP_ALL", "Date_ \"Date_\" true true false 10 Long 0 10 ,First,#,C:\\Users\\Forest\\Desktop\\saguaro_detection\\Ortho2011_FlightPoints\\Pima_Photos_2011.shp,Date_,-1,-1;GPSTime \"GPSTime\" true true false 19 Double 0 0 ,First,#,C:\\Users\\Forest\\Desktop\\saguaro_detection\\Ortho2011_FlightPoints\\Pima_Photos_2011.shp,GPSTime,-1,-1;TOWNSHIP \"TOWNSHIP\" true true false 4 Text 0 0 ,First,#,C:\\Users\\Forest\\Desktop\\saguaro_detection\\township_range_az\\trs.shp,TOWNSHIP,-1,-1;RANGE \"RANGE\" true true false 4 Text 0 0 ,First,#,C:\\Users\\Forest\\Desktop\\saguaro_detection\\township_range_az\\trs.shp,RANGE,-1,-1;SECTION \"SECTION\" true true false 2 Text 0 0 ,First,#,C:\\Users\\Forest\\Desktop\\saguaro_detection\\township_range_az\\trs.shp,SECTION,-1,-1", "INTERSECT", "", "")

# Process: Add Field
arcpy.AddField_management(output, "az2", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (2)
arcpy.AddField_management(output, "eastwest", "STRING", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (3)
arcpy.AddField_management(output, "TILE_NAME", "STRING", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (4)
arcpy.AddField_management(output, "localhour", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (5)
arcpy.AddField_management(output, "solaralt", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

finames=['GPSTime', 'Date_', 'az2','eastwest', 'TILE_NAME','TOWNSHIP','RANGE','SECTION','localhour','solaralt']
rows = arcpy.da.UpdateCursor(output,finames)
for row in rows:
    hourraw=(row[0]%(3600*24))/3600
    hour=int(hourraw)
    day=str(row[1])
    year=day[:4]
    month=day[4:6]
    dayy=day[6:]
    minute=60*(hourraw-hour)

    solarazi = Pysolar.solar.GetAzimuth(locallat,locallong,datetime.datetime(int(year), int(month), int(dayy), int(hour), int(minute)))

    solaralt = Pysolar.solar.GetAltitude(locallat,locallong,datetime.datetime(int(year), int(month), int(dayy), int(hour), int(minute)))

    row[2]=solarazi 
    row[9]=solaralt

    if solarazi<-180:
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
