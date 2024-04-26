## Copyright Pat Hall, 2024. ##
## Last Updated 04.25.24 ##

#this file creates a canopy height model using the tools defined in tools.py

import tools
from dotenv import load_dotenv
import os

load_dotenv()

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

selection = 0

while selection == 0:
    
    selection = int(input("Enter selection: "))
    print()

    if selection != 0:
        break
    
    else:
        print()
        print("You entered an invalid option. Please choose from the provided options.")
        print("---")
        print('Enter the number of the option you would like to select:')
        print('(1) single file')
        print('(2) folder of files')
        selection = 0

out_name = input("Please enter name of output file (do not include extension): ") + '.tif'
print()

## ADD ERROR HANDLING HERE ##

if selection == 1:
    print("executing CHM creation for 1 file...")
    out_dtm,out_dsm,out_filepath = tools.execute_pl()
    tools.create_chm(out_dtm,out_dsm,out_name,out_filepath)

    



