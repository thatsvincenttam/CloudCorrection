#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maithya
#
# Created:     27/04/2017
# Copyright:   (c) Maithya 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys
import logging
import traceback
import numpy as np
from osgeo import gdal

def getGainAndOffset(baseName,directoryName,textSuffix):
    ##List as follows
    ## basename
    ## directoryName
    ## fileExtension
    ## bandNumber
    ## textfile for metadata
    ## gain
    ## offset
    paramList=[]

    ##Raster File Name : LC08_L1TP_166063_20170418_20170418_01_RT_B8.TIF | Directory : E:\GIS Data\DAVVOC\Maithya\Images\LC08_L1TP_166063_20170418_20170418_01_RT

    #Get band number
    band =baseName.split("_")#Split by underscore*
    s = band[int(len(band) -1)]#get last component. looks like "B8.TIF"
    band =s.split(".")#Split by period*
    s = band[0]#Get first element in the list . looks like "B8"
    bandNumber = s[1:] #get the band number

    #Construct textfile name
    directorypath = directoryName.split(os.path.sep) #Split using OS separator
    commonFileName = directorypath[int(len(directorypath) -1)]#get common file name
    textfile =commonFileName + textSuffix

    filepath = os.path.join(directoryName, textfile)
    gainAndOffset = readGainAndOffsetFromMetadataFile(filepath,bandNumber)
    if  gainAndOffset != []:
            paramList.append(baseName)
            paramList.append(directoryName)
            paramList.append("TIF")
            paramList.append(bandNumber)
            paramList.append(textfile)
            paramList.append(gainAndOffset[0])
            paramList.append(gainAndOffset[1])
            
    #
    return paramList

def readGainAndOffsetFromMetadataFile(filepath,bandNumber):
    gainAndOffset=[]
    s = ""
    paramOfInterest = ""
    multiBand = ""
    addBand = ""

    with open(filepath) as f:
        for line in f:
            s =line.rstrip().lstrip()
            param = s.split("=")

            paramOfInterest =str(param[0]).rstrip().lstrip()
            multiBand = "REFLECTANCE_MULT_BAND_"+ bandNumber
            addBand = "REFLECTANCE_ADD_BAND_"+ bandNumber

            if paramOfInterest== multiBand:
                gainAndOffset.append(param[1])
            if paramOfInterest== addBand:
                gainAndOffset.append(param[1])
            #print(s)

    return gainAndOffset

def checkIfDirectoryExists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return ""

def saveImage(npdata,_rows,_cols,_trans,_proj,_nodatav,outfilename,directory):
    try:
        #Create file using information from Original File
        rasterFilePath = os.path.join(directory, "Reflectance_" + outfilename)
        
        outDrive = gdal.GetDriverByName("GTiff")  
        outRaster = outDrive.Create(str(rasterFilePath),_rows,_cols,1,gdal.GDT_Float32)

        #Write array to the file
        outRaster.GetRasterBand(1).WriteArray(npdata)

        #Seta no data value
        outRaster.GetRasterBand(1).SetNoDataValue(_nodatav)

        #GeoReference the image
        outRaster.SetGeoTransform(_trans)

        #Write projection information
        outRaster.SetProjection(_proj)

        #Flush out
        outRaster = None
        
    except:
        ## Return any Python specific errors and any error returned
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        pymsg = "PYTHON ERRORS:\n  Function save_image( npdata, outfilename) \n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        ##Write to the error log file
        logger_error.info( pymsg)    
    return ""

def main():
    pass

if __name__ == '__main__':
    main()