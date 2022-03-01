def main():
    import os
    import arcpy
    inFolder = "c:\\users\\james\\documents\\crane_mills_lidar\\lidar"

    from arcpy import env
    env.workspace = "c:\\users\\james\\documents\\crane_mills_lidar\\lidar"

    # get a list of files
    listOfFiles = os.listdir(inFolder)

    for file in listOfFiles:

        inFile = inFolder + "\\" + file

        # add file to dataset
        print(inFile)
        arcpy.management.CreateLasDataset(inFile,"test.lasd")
        arcpy.MakeLasDatasetLayer_management('test.lasd', 'Cat_1_2_Layer', [1, 2], "", "EXCLUDE_UNFLAGGED",
                                             "EXCLUDE_SYNTHETIC","EXCLUDE_KEYPOINT", "EXCLUDE_WITHHELD", "", "EXCLUDE_OVERLAP")

        #classify buildings
        arcpy.ClassifyLasBuilding_3d('Cat_1_2_Layer',min_height="3",min_area='10',classify_above_roof=True,above_roof_height=10,
        above_roof_code=6,classify_below_roof=True,below_roof_code=6)

        # write the sub dataset to a new file
        arcpy.ddd.ExtractLas('Cat_1_2_Layer', "c:\\users\\james\\documents\\crane_mills_lidar_processed", "",name_suffix="_NoNoiseOverlap_Classified")

        arcpy.management.Delete('Cat_1_2_Layer')
        arcpy.management.Delete("test.lasd")
        print (file)

    for file in listOfFiles:
        inFile = inFolder + "\\" + file
        os.remove(inFile + "x")
        os.remove("c:\\users\\james\\documents\\crane_mills_lidar_processed\\" + file.strip(".las") + "_NoNoiseOverlap_Classified.lasx")

main()
