## Copyright Pat Hall, 2024. ##
## Last Updated 04.27.24 ##

#this file creates a canopy height model using the functions defined in tools.py

import tools
from dotenv import load_dotenv
import os
import rasterio

#cm() stands for CanopyModel. This function combines the functions from tools.py to create a program with commandline interaction.
def cm():
    #dotenv file probably unecessary - at the moment it just contains the DEBUG variable.
    load_dotenv()
    
    chm_name = None
    out_filepath = None
    input_folderpath = None

    #sets DEBUG variables for a quick run when DEBUG is set to True.
    debug_state = os.getenv("DEBUG")
    if debug_state  == 'True':
        chm_name = "test_chm.tif"
        out_filepath = "/Users/pathall/Documents/CanopyModel_PDAL/Output"
        input_folderpath = '/Users/pathall/Documents/CanopyModel_PDAL/LiDAR_multi_test'


    ##PART 1: Select Process
    #Currently, 3 is the value used if you want to exit the program. The program will loop until 3 is selected.
    selection = 0

    while selection != 3:

        print('CanopyModeler. Created by Pat Hall. Copyright 2024.')
        print('---')
        print('This tool takes a folder of .las or .laz point-cloud LiDar files and returns')
        print('a single canopy height model raster as a GeoTiff file.')
        print()

        print('Would you like to create a Canopy Height Model from a single file or a folder?')
        print()
        print('Enter the number of the option you would like to select:')
        print('(1) single file')
        print('(2) folder of files')
        print('(3) end program')


        #This while loop is for error handling - make sure the user enters one of the provided options.
        while selection == 0:
            
            selection = int(input("Enter selection: "))
            print()

            if selection == 1 or selection == 2 or selection == 3:
                break
            
            #if selection is not a valid option, the user is looped back to the text prompting a selection.
            else:
                print()
                print("You entered an invalid option. Please choose from the provided options.")
                print("---")
                print('Enter the number of the option you would like to select:')
                print('(1) single file')
                print('(2) folder of files')
                print('(3) exit program')
                #set selection back to 0 to ensure the loop occurs.
                selection = 0

        #chm_name will be the name of the final output. in the case of processing a single file,
        #the single output chm will use this name. for the multi laz file option, the merged output
        #will take this name.
        #chm_name will not be set to None if DEBUG == 'True'
        if chm_name == None:
            chm_name = input("Please enter name of output file (do not include extension): ") + '.tif'
            print()

        ## ADD ERROR HANDLING HERE ##

        ##PART 2: Single file CHM creation
        if selection == 1:
            print("executing CHM creation for 1 file...")

            #out_dtm and out_dsm are both .tif raster files. processes can be viewed in the JSON pipeline files
            #dtm.json and dsm.json. 
            out_dtm,out_dsm,out_filepath = tools.execute_pl(out_filepath=out_filepath)

            #tools.create_chm produces the chm from the dtm and dsm .tif raster generated by tools.execute_pl() 
            tools.create_chm(out_dtm,out_dsm,out_filepath,out_name=chm_name)
            selection = 0 #Loops back to program selection.

        ##PART 3: Multi-file CHM Creation
        elif selection == 2:
            #identifies LiDAR files, and puts them in a list as filepaths.
            file_list, file_count = tools.identify_li_files(folderpath=input_folderpath)

            #prompts user for the out filepath if it has not already been specified.
            if out_filepath == None:
                out_filepath = r'{}'.format(input('Enter the path to the folder for output files: ').strip('"\''))

            #process_counter allows a readout of how many files have been processed.
            process_counter = 0

            #error handling - we only want to process folders with valid .tif files.
            #break brings us back to program selection.
            if file_count == 0:
                print('The folder you specified has no compatible files. (.laz, .las)')
                break
            
            #tell user how many files are being processed.
            else:
                print(f'Executing CHM creation from {file_count} files')
                print('---')

            #for loop to convert LiDAR files first to DTM and DSMs and then to A single CHM.
            #DSM and DTM file are overwritten in each pass.
            for file in file_list:
                process_counter += 1
                file_name = str(os.path.basename(file))

                #Adds '_CHM.tif' to the output name so that the out rasters have the 
                #same name as the in LiDAR tiles
                file_name_tif_extension = tools.chm_got_the_tif_bug(file_name)

                #ignore_me is the out_Filepath retrun from execute_pl(). Necessary for Selection 1, not for selection 2.
                print(f'processing file {process_counter} of {file_count}.')
                out_dtm, out_dsm, ignore_me = tools.execute_pl(lidar_filepath = file,out_filepath=out_filepath)
                print()

                #creates the CHM .tif
                tools.create_chm(out_dtm,out_dsm,out_filepath,out_name=file_name_tif_extension)

            #sets the crs to out_dtm.tif (both tif's should have the same crs)
            crs = (rasterio.open(out_dtm)).crs

            #delete the intermidiate dtm and dsm tif files
            os.remove(out_dtm)
            os.remove(out_dsm)


            print()
            print(f'succesfully processed {file_count} files.')
            print()
            print(f'mosaicking {file_count} files...')

            #joins final output name to filepath for megred chm
            out_file_destination = os.path.join(out_filepath,chm_name)

            #adds filepaths for all files to a list for merging.
            tif_filelist = tools.identify_tif_files(out_filepath)

            #merges chm files, and writes to a new tif.
            tools.merge_chm(tif_filelist,out_file_destination,crs)
            print('mosaicking completed successfully.')

            #loop back to program selection
            selection = 0

        elif selection == 3:
            print("exit program.")
            break





            



