#Created by James Balcomb March 4 2020
#The lidar files to be processed must be in .las format

#A bunch of .lasx files will be created by the process.
#The script will delete those but if it crashes you will need to delete them
# using windows explorer.

def main():

    inFolder, outFolder, shpFile = gatherInput()

    listOfLasFiles = makeListOfLasFiles(inFolder)

    results = open(outFolder + "\\" + "results.txt", 'w')
    results.write("ORIGINAL LAS FILES #######################################\n")
    results.close()

    analyzeLidar(inFolder, listOfLasFiles, outFolder)

    if (inFolder == "q") or (outFolder == "q") or (shpFile == "q"):
        print ("Ending script")
    else:
        processLidar(outFolder, listOfLasFiles, inFolder, shpFile)

    #update list of las files to processed files
    processedListOfLasFiles = []

    for file in listOfLasFiles:
        processedListOfLasFiles.append(file.strip(".las") + "_NoNoiseOverlap_Classified.las")

    analyzeLidar(outFolder, processedListOfLasFiles, outFolder)




def gatherInput():

    import os
    inFolder = ""

    while (inFolder != "q") and (os.path.exists(inFolder) == False):
        inFolder = str.lower(input("Please enter the full pathway of the folder containing files to be processed or " +
                                   "q to quit. Use the following format.. c:\\users\\NikkiIsAwsome\\craneMills\n"))
        #inFolder = "c:\\users\\james\\documents\\crane_mills_lidar\\lidar"

    outFolder = ""

    while (outFolder != "q") and (os.path.exists(outFolder) == False):
        outFolder = str.lower(input("Please enter the full pathway of the destination folder for the files to be processed or " +
                                   "q to quit. Use the following format.. c:\\users\\NikkiIsAwsome\\craneMills\n"))
        #outFolder = "c:\\users\\james\\documents\\crane_mills_lidar\\processed"


    shpFile = ""

    while (shpFile != "q") and (os.path.exists(shpFile) == False):

        shpFile = str.lower(input("Please enter the full pathway of the boundary clip shapefile or " +
                                   "q to quit. Use the following format.. c:\\users\\NikkiIsAwsome\\example.shp\n"))
        #shpFile = "c:\\users\\james\\documents\\crane_mills_lidar\\main_block\\main_block.shp"

    print ("Please wait...")

    return (inFolder, outFolder, shpFile)

def makeListOfLasFiles(inFolder):

    import os
    listOfLasFiles = []

    # get a list of files
    listOfFiles = os.listdir(inFolder)

    for file in listOfFiles:

        if (os.path.isfile(inFolder + "\\" + file)) == True:
            fileExt = file.split(".")
            fileExt = fileExt[1]

            if fileExt == "las":
                listOfLasFiles.append(file)

    return listOfLasFiles

def analyzeLidar(inFolder, listOfLasFiles, outFolder):

    import arcpy
    import os

    # set the workspace
    arcpy.env.workspace = inFolder

    # create las dataset
    arcpy.management.CreateLasDataset(inFolder, "stats.lasd", "", "", "", "", "", "NO_FILES")

    for file in listOfLasFiles:

        arcpy.management.AddFilesToLasDataset(in_las_dataset="stats.lasd", in_files=file)
        print(inFolder + "\\" + file + "x")
        os.remove(inFolder + "\\" + file + "x")

    arcpy.management.LasDatasetStatistics(in_las_dataset="stats.lasd", out_file="tempResults.txt")

    #read temp results
    temp = open(inFolder + "\\" + "tempResults.txt")

    results = open(outFolder + "\\" + "results.txt", 'a')
    for line in temp:
    #add to results.txt
        results.write(line + '\n')

    results.write("PROCESSED LAS FILES #####################################")
    results.close()
    temp.close()

    #delete temp files
    arcpy.management.Delete("stats.lasd")
    os.remove(inFolder + "\\" + "tempResults.txt.xml")
    os.remove(inFolder + "\\" + "tempResults.txt")

    for file in listOfLasFiles:
        os.remove(inFolder + "\\" + file + "x")

def processLidar(outFolder, listOfLasFiles, inFolder, shpFile):

    import os
    import arcpy
    from arcpy import env
    env.workspace = outFolder

    length = len(listOfLasFiles)
    number = 0

    for file in listOfLasFiles:

        inFile = inFolder + "\\" + file

        # add file to dataset
        number = number + 1
        print ("Processing " + str(number) + " of " + str(length))

        print("Processsing", inFile)
        arcpy.management.CreateLasDataset(input=inFile,out_las_dataset="test.lasd")
        arcpy.MakeLasDatasetLayer_management('test.lasd', 'Cat_1_2_Layer', [1, 2], "", "INCLUDE_UNFLAGGED",
                                     "EXCLUDE_SYNTHETIC","EXCLUDE_KEYPOINT", "EXCLUDE_WITHHELD", "", "EXCLUDE_OVERLAP")

        # classify buildings
        arcpy.ClassifyLasBuilding_3d('Cat_1_2_Layer', min_height="3", min_area='10', classify_above_roof=True,
                                     above_roof_height=10,
                                     above_roof_code=6, classify_below_roof=True, below_roof_code=6)

        # write the sub dataset to a new file
        print ("Saving to " + outFolder)
        arcpy.ddd.ExtractLas('Cat_1_2_Layer', target_folder=outFolder,
                             name_suffix="_NoNoiseOverlap_Classified", boundary=shpFile)

        arcpy.management.Delete('Cat_1_2_Layer')
        arcpy.management.Delete("test.lasd")

        os.remove(inFile + "x")

        try:
            os.remove(outFolder + "\\" + file.strip(".las") + "_NoNoiseOverlap_Classified.lasx")

        except FileNotFoundError:
            print ("That file was not in the study area\n")





main()
