# CanopyModel_PDAL
This is a Python repository that utilizes the PDAL library to automate the process of creating Tree Canopy models from LiDAR LAZ files.

run_cm.py is a file that runs all the functions required to make Canopy Height Models (CHM).

CanopyModel.py is the Python script that allows for user interaction in the commandline. It strings together functions from tools.py to create a single CHM from a single LAZ file or a whole folder of LAZ files.

tools.py contains all the functions used to create the CHM files. the functions contained in this file include filelist compilers and wrapper functions for PDAL.

dsm.json and dtm.json are pipeline files that set the processes and parameters for interpolating DSM and DTM rasters from the initial LAZ point-cloud data.

This program is being developed and tested for use on a Mac running OS X Sonoma. The files are written by Pat Hall. 2024.

Connect with me on [LinkedIn](https://www.linkedin.com/in/pjh-geospatial/)


# References 
_Band Math w. Rasterio—Python Open Source Spatial Programming & Remote Sensing._
  _(n.d.). Retrieved April 22, 2024, from https://pygis.io/docs/e_raster_math.html_

_Bell, A., Chambers, B., Butler, H., & Others. (2024). About—Pdal.io [Documentation]._ 
  _Pdal.Io. https://pdal.io/en/2.7-maintenance/about.html_

_LAS Specification 1.4- R14. (2019). The American Society for Photogrammetry & Remote_
  _Sensing. https://www.asprs.org/wp-content/uploads/2019/03/LAS_1_4_r14.pdf_

_Mann, M., Chao, S., Graesser, J., & Feldman, N. (n.d.). (2023) PyGIS - Python Open Source_ 
  _Spatial Programming & Remote Sensing [Textbook]. PyGIS.Io. Retrieved May 7, 2024, from https://pygis.io/docs/a_intro.html#_

_McGaughey, R. J. (2023). FUSION/LDV: Software for LIDAR Data Analysis and_ 
  _Visualization. United States Department of Agriculture. http://forsys.sefs.uw.edu/software/fusion/FUSION_manual.pdf_

_Planzer, S. (2020, May 7). Producing a Canopy Height Model (CHM) from LiDAR_ 
_[Portfolio]. Simonplanzer.Com. https://www.simonplanzer.com/articles/lidar-chm/_

_SciPy User Guide—SciPy v1.13.0 Manual. (2024). [Documentation]. SciPy User Guide._ 
  _https://docs.scipy.org/doc/scipy/tutorial/index.html_

_Tenkanen, H. (2018). Creating a raster mosaic—Intro to Python GIS documentation_ 
  _[Education Course]. Intro to Python GIS. https://automating-gis-processes.github.io/CSC18/lessons/L6/raster-mosaic.html_

_What is NumPy? —NumPy v1.26 Manual. (2022). Numpy.Org._ 
  _https://numpy.org/doc/stable/user/whatisnumpy.html_







