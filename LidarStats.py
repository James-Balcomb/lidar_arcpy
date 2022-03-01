def main():
    import os
    import arcpy
    inFolder = "c:\\users\\james\\documents\\crane_mills_lidar_processed"

    # set the workspace
    arcpy.env.workspace = inFolder

    # set the spatial reference
    sr = arcpy.SpatialReference("WGS 1984 UTM Zone 10N")  # , "NAVD88_height_(ftUS)")

    # create las dataset
    arcpy.management.CreateLasDataset(inFolder, "initial_stats.lasd", "", "", "", "", "", "NO_FILES")

    arcpy.management.LasDatasetStatistics(in_las_dataset="initial_stats.lasd", out_file="initialStats.txt")

    print ('Done')

main()