## Copyright Pat Hall, 2024. ##
## Last Updated 04.25.24 ##

#this file creates a canopy height model using the tools defined in tools.py

import tools
from dotenv import load_dotenv
import os
def cm():
    load_dotenv()
    
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

        chm_name = input("Please enter name of output file (do not include extension): ") + '.tif'
        print()

        ## ADD ERROR HANDLING HERE ##

        if selection == 1:
            print("executing CHM creation for 1 file...")
            out_dtm,out_dsm,out_filepath = tools.execute_pl()
            tools.create_chm(out_dtm,out_dsm,out_filepath,out_name=chm_name)

        elif selection == 2:
            file_list, file_count = tools.identify_li_files()
            process_counter = 0

            if file_count == 0:
                print('The folder you specified has no compatible files. (.laz, .las)')
                break

            else:
                print(f'Executing CHM creation from {file_count} files')
                print('---')

            for file in file_list:
                process_counter += 1
                file_name = tools.chm_got_the_tif_bug(file)

                print(f'processing file {process_counter} of {file_count}.')
                out_dtm, out_dsm, out_filepath = tools.execute_pl(lidar_filepath = file)
                print()
                tools.create_chm(out_dtm,out_dsm,out_filepath,out_name=file_name)





            



