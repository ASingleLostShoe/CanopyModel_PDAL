## Copyright Pat Hall, 2024. ##
## Last Updated 04.27.24 ##

#this file creates a canopy height model using the functions defined in tools.py

import tools
from dotenv import load_dotenv
import os
import rasterio

def cm():
    load_dotenv()
    
    chm_name = None
    out_filepath = None
    input_folderpath = None


    debug_state = os.getenv("DEBUG")
    if debug_state  == 'True':
        chm_name = "test_chm.tif"
        out_filepath = "/Users/pathall/Documents/CanopyModel_PDAL/Output"
        input_folderpath = '/Users/pathall/Documents/CanopyModel_PDAL/LiDAR_multi_test'


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



        while selection == 0:
            
            selection = int(input("Enter selection: "))
            print()

            if selection == 1 or selection == 2 or selection == 3:
                break
            
            else:
                print()
                print("You entered an invalid option. Please choose from the provided options.")
                print("---")
                print('Enter the number of the option you would like to select:')
                print('(1) single file')
                print('(2) folder of files')
                print('(3) exit program')
                selection = 0

        if chm_name == None:
            chm_name = input("Please enter name of output file (do not include extension): ") + '.tif'
            print()

        ## ADD ERROR HANDLING HERE ##

        if selection == 1:
            print("executing CHM creation for 1 file...")
            out_dtm,out_dsm,out_filepath = tools.execute_pl()
            tools.create_chm(out_dtm,out_dsm,out_filepath,out_name=chm_name)
            selection = 0

        elif selection == 2:
            file_list, file_count = tools.identify_li_files(folderpath=input_folderpath)
            if out_filepath == None:
                out_filepath = r'{}'.format(input('Enter the path to the folder for output files: ').strip('"\''))

            process_counter = 0

            if file_count == 0:
                print('The folder you specified has no compatible files. (.laz, .las)')
                break

            else:
                print(f'Executing CHM creation from {file_count} files')
                print('---')

            for file in file_list:
                process_counter += 1
                file_name = str(os.path.basename(file))
                file_name_tif_extension = tools.chm_got_the_tif_bug(file_name)

                print(f'processing file {process_counter} of {file_count}.')
                out_dtm, out_dsm, ignore_me = tools.execute_pl(lidar_filepath = file,out_filepath=out_filepath)
                print()
                tools.create_chm(out_dtm,out_dsm,out_filepath,out_name=file_name_tif_extension)

            crs = (rasterio.open(out_dtm)).crs
            os.remove(out_dtm)
            os.remove(out_dsm)

            print()
            print(f'succesfully processed {file_count} files.')
            print()
            print(f'mosaicking {file_count} files...')
            out_file_destination = os.path.join(out_filepath,chm_name)
            tif_filelist = tools.identify_tif_files(out_filepath)
            tools.merge_chm(tif_filelist,out_file_destination,crs)
            print('mosaicking completed successfully.')

            selection = 0

        elif selection == 3:
            print("exit program.")
            break





            



