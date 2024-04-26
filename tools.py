## Copyright by Pat Hall, 2024. ##
## Last Updated 04.25.24 ##

#This file defines functions used in the main program.

import json
import pdal
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os

#opens specified JSON file containing the pdal pipeline and reads it into a python dictionary file
#which can be executed elsewhere. "pl" stands for "pipeline".
def open_pipeline(pipeline_file):
    with open(pipeline_file,'r') as pipeline: #open json file
        pl = json.load(pipeline) #load json file into python dict
        return pl
        
#takes the json pipelines as a list of dictionaries, inserts input and output filepaths, converts to a 
#pdal pipeline object, and executes. outputs two .tif files (DTM and DSM) and returns their parent directory filepath. 
def execute_pl(dtm_json = 'dtm.json', dsm_json = 'dsm.json'):
        
        ## Add option to keep intermidiate files (dsm,dtm) ##

        out_dsm_name = 'out_dsm.tif'
        out_dtm_name = 'out_dtm.tif'

        #Requests the user for input and output filepaths.

        lidar_filepath = r'{}'.format(input('Enter path to LiDAR file: ').strip('"\''))
        print()
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
def create_chm(dtm,dsm,out_name,out_filepath):
    #this function utilizes rasterio, a python library that allows the manipulation of rasters as numpy arrays.

    raster_destination = os.path.join(out_filepath,out_name) #output CHM location + file name

    raster_specs = rasterio.open(dtm) #opens dtm as a raster
    raster_crs = raster_specs.crs #stores the Coordinate reference System for dtm (will be the same for both dtm and dsm)
    raster_transform = raster_specs.transform #stores the transform for dtm (will be the same for both dtm and dsm)

    #read stored dtm and dsm rasters (.tif format) into numpy arrays
    raster_dtm = rasterio.open(dtm).read(1)
    raster_dsm = rasterio.open(dsm).read(1)

    #create CHM using array arithmetic. CHM = DSM - DTM
    raster_chm = raster_dsm - raster_dtm

    #mask null values, and values we don't want to include in our canopy.
    #all pixels with a value of less than 1.83 meters (6 feet) will be excuded from the out chm raster.
    mask_null = (raster_dsm == -10) | (raster_dtm == -10)
    mask_small = (raster_chm <1.83)
    raster_chm[mask_null] = 0
    raster_chm[mask_small] = 0

    #writes the chm numpy array to a new geotiff file at the out_filepath location.
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
         dst.close


