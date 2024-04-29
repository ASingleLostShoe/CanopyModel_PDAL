## Copyright by Pat Hall, 2024. ##
## Last Updated 04.27.24 ##

#This file defines functions used in the main program.

import json
import pdal
import rasterio
from rasterio.merge import merge
import numpy as np
import matplotlib.pyplot as plt
import os
import rasterio.merge

#opens specified JSON file containing the pdal pipeline and reads it into a python dictionary file
#which can be executed elsewhere. "pl" stands for "pipeline".
def open_pipeline(pipeline_file):
    with open(pipeline_file,'r') as pipeline: #open json file
        pl = json.load(pipeline) #load json file into python dict
        return pl
        
#takes the json pipelines as a list of dictionaries, inserts input and output filepaths, converts to a 
#pdal pipeline object, and executes. outputs two .tif files (DTM and DSM) and returns their parent directory filepath. 
def execute_pl(dtm_json = 'dtm.json', dsm_json = 'dsm.json',out_filepath = None, lidar_filepath = None):
        
        ## Add option to keep intermidiate files (dsm,dtm) ##

        out_dsm_name = 'out_dsm.tif'
        out_dtm_name = 'out_dtm.tif'

        #Requests the user for input and output filepaths.

        if lidar_filepath == None:
            lidar_filepath = r'{}'.format(input('Enter path to LiDAR file: ').strip('"\''))
            print()
        if out_filepath == None:    
            out_filepath = r'{}'.format(input('Enter the path to the folder for output files: ').strip('"\''))
            print()

        ## ERROR HANDLING HERE ##
        
        out_dtm = os.path.join(out_filepath,out_dtm_name)
        out_dsm = os.path.join(out_filepath,out_dsm_name)

        #open jsons as lists of dictionaries.
        print("accessing pdal processing pipelines...")
        dtm_pl = open_pipeline(dtm_json)
        dsm_pl = open_pipeline(dsm_json)
        print("pdal pipelines succesfully accessed.")
        print()

        #insert input filepath into pipeline.
        print("inserting LiDAR filepath into pipelines...")
        dtm_pl[0]["filename"] = lidar_filepath
        dsm_pl[0]["filename"] = lidar_filepath
        print("LiDAR filepath inserted successfully.")
        print()

        #insert output filepath into pipline.
        print("inserting output filepath into pipelines...")
        dtm_pl[2]["filename"] = out_dtm
        dsm_pl[2]["filename"] = out_dsm
        print("output filepaths inserted succesfully.")
        print()


        #utilize pdal library to store dict lists as pdal pipleine objects.
        print("finalizing pipelines...")
        dtm_pl = json.dumps(dtm_pl)
        dsm_pl = json.dumps(dsm_pl)
        pipeline_dsm = pdal.Pipeline(dsm_pl)
        pipeline_dtm = pdal.Pipeline(dtm_pl)

        #Execute pipelines, producing dtm and dsm.
        print("Processing DSM...")
        pipeline_dsm.execute()
        print(f"DSM created at location {out_filepath}.")
        print()
        print("Processing DTM...")
        pipeline_dtm.execute()
        print(f"DTM created at location {out_filepath}.")

        return out_dtm,out_dsm,out_filepath

# Generates CHM from derived DTM and DSM created in execute_pl
def create_chm(dtm,dsm,out_filepath,out_name = None):
    #this function utilizes rasterio, a python library that allows the manipulation of rasters as numpy arrays.


    raster_destination = os.path.join(out_filepath,out_name) #output CHM location + file name

    print('Consolidating georeferencing specifications...')
    print('     opening reference raster...')
    raster_specs = rasterio.open(dtm) #opens dtm as a raster
    print(f'    storing coordinate reference system for {out_name}.laz...')
    raster_crs = raster_specs.crs #stores the Coordinate reference System for dtm (will be the same for both dtm and dsm)
    print(f'    storing transform for {out_name}.laz...')
    raster_transform = raster_specs.transform #stores the transform for dtm (will be the same for both dtm and dsm)
    print('georeferencing specifications consolidated.')
    print()


    #read stored dtm and dsm rasters (.tif format) into numpy arrays
    print('reading dtm raster into numpy array...')
    raster_dtm = rasterio.open(dtm).read(1)
    print('success.')
    print()
    print('reading dsm raster into numpy array...')
    raster_dsm = rasterio.open(dsm).read(1)
    print('success.')
    print()

    print('validating array shapes...')
    raster_dtm_validated, raster_dsm_validated = check_array_sizes(raster_dtm,raster_dsm)
    raster_dtm = raster_dtm_validated
    raster_dsm = raster_dsm_validated

    #create CHM using array arithmetic. CHM = DSM - DTM
    print('subtracting dtm from dsm...')
    raster_chm = raster_dsm - raster_dtm
    print('success.')
    print()

    #mask null values, and values we don't want to include in our canopy.
    #all pixels with a value of less than 1.83 meters (6 feet) will be excuded from the out chm raster.
    print('Identifying null values and small vegetation for exclusion...')
    mask_null = (raster_dsm == -10) | (raster_dtm == -10)
    mask_small = (raster_chm <1.83)
    print('success.')
    print()
    print('applying mask to chm array...')
    raster_chm[mask_null] = 0
    raster_chm[mask_small] = 0
    print('success.')
    print()

    #writes the chm numpy array to a new geotiff file at the out_filepath location.
    print(f'writing chm to GTiff raster format at {raster_destination}...')
    with rasterio.open(
         raster_destination,
         'w',
         driver='GTiff',
         height=raster_chm.shape[0],
         width=raster_chm.shape[1],
         count=1,
         dtype=raster_dtm.dtype,
         crs=raster_crs,
         transform=raster_transform
    ) as dst:
         dst.write(raster_chm,1)
         print('chm raster successfully produced.')
         dst.close
         print('raster file connection closed.')

    

#Returns a list of all files in a folder that use the .laz or .las extension.
def identify_li_files(folderpath=None):
    if folderpath == None:
        folderpath = r'{}'.format(input('Enter the path to the folder with files for processing: ').strip('"\''))

    
    print('Compilating LiDAR files in specified folder...')
    #create list for filepaths to be appended to
    laz_las_filelist = []

    #for loop crawls files in directory at specified folder path. For any files that end with 
    #'.laz' or '.las', the file path is appended to the filelist.
    for file in os.listdir(folderpath):
        if file.endswith('.laz') or file.endswith('.las'):
            laz_las_filelist.append(os.path.join(folderpath,file))

    file_count = len(laz_las_filelist)
    
    print(f'{file_count} files compilated.')
    print()

    return laz_las_filelist, file_count

#strips file extension from a file name and replaces it with '_chm.tif' extension. Useful 
#for giving output tifs the same name as input .laz files, and identifying they are output chm.   
def chm_got_the_tif_bug(string):
     string_no_file_extension = string.rsplit('.',1)
     string_got_the_tif = str(string_no_file_extension) + '_chm.tif'
     return string_got_the_tif

#used to check that dsm and dtm are the same array shape after laoding into a numpy aray. 
#Prevents errors in the subtraction portion of create_chm()
def check_array_sizes(np1,np2):

    # Find the difference in shape
    diff_rows = np2.shape[0] - np1.shape[0]
    diff_cols = np2.shape[1] - np1.shape[1]

    # Add zero-value rows and columns to the smaller array
    if diff_rows > 0:
        zeros = np.zeros((diff_rows, np1.shape[1]))
        np1 = np.vstack((np1, zeros))
        print(f'dtm corrected by {diff_rows} rows.')

    if diff_cols > 0:
        zeros = np.zeros((np1.shape[0], diff_cols))
        np1 = np.hstack((np1, zeros))
        print(f'dtm corrected by {diff_cols} columns.')

    if diff_rows < 0:
        zeros = np.zeros((-diff_rows, np2.shape[1]))
        np2 = np.vstack((np2, zeros))
        print(f'dsm corrected by {-diff_rows} rows.')

    if diff_cols < 0:
        zeros = np.zeros((np2.shape[0], -diff_cols))
        np2 = np.hstack((np2, zeros))
        print(f'dsm corrected by {-diff_cols} columns.')

    #print(f'dtm array shape: ({np1.shape[0],np1.shape[1]})')
    #print(f'dsm array shape: ({np2.shape[0],np2.shape[1]})')

    return np1,np2

#Creates a list of tif files in a directory. used for collating list of 
#output CHM raster to be merged.
def identify_tif_files(folderpath = None):
    if folderpath == None:
        folderpath = r'{}'.format(input('Enter the path to the folder with files for merging: ').strip('"\''))

    
    print(f'Compiling tif files at {folderpath}...')
    #create list for filepaths to be appended to
    tif_filelist = []

    #for loop crawls files in directory at specified folder path. For any files that end with 
    #'.laz' or '.las', the file path is appended to the filelist.
    for file in os.listdir(folderpath):
        if file.endswith('.tif'):
            tif_filelist.append(os.path.join(folderpath,file))

    file_count = len(tif_filelist)
    
    print(f'{file_count} files compiled for merge.')
    print()

    return tif_filelist

#merges a list of raster files into a single raster, then writes out as GTiff to a 
#specified destination.
def merge_chm(chm_filelist,raster_destination,out_crs):
    #create empty list for open raster objects
    rasters_to_mosaic = []

    #open all rasters in chm_fileist as open rasters using rasterio
    for chm_raster in chm_filelist:
        raster_open = rasterio.open(chm_raster)
        rasters_to_mosaic.append(raster_open)

    merged_chm, out_trans = merge(rasters_to_mosaic)

    """
    sqz_merged_chm = np.squeeze(merged_chm,axis=0)

    print(sqz_merged_chm.shape[0],sqz_merged_chm.shape[1])
    print(out_trans)
    plt.imshow(sqz_merged_chm)
    plt.show()
    """
    
    with rasterio.open(
         raster_destination,
         'w',
         driver='GTiff',
         height=merged_chm.shape[1],
         width=merged_chm.shape[2],
         count=1,
         dtype=merged_chm.dtype,
         crs=out_crs,
         transform=out_trans
    ) as dst:
         dst.write(merged_chm)
         print(f'{len(rasters_to_mosaic)} chm rasters successfully merged.')
         dst.close
         print('raster file connection closed.')
    