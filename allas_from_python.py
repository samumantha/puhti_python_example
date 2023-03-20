#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Examples on how to use files from Allas object storage directly from Puhti

Author: Kylli Ek, Samantha Wittke, CSC

'''

# The required packages depend on the task
import os
# For working with rasters
import rasterio
# For working with vector data
import geopandas as gpd
# For working with object storage
import boto3


# Before starting to use Allas with S3 set up your connection to Allas.
# In Puhti run:
#
# module load allas
# allas-conf --mode s3cmd


# Reading raster file directly from Allas using rasterio

open_raster = rasterio.open('/vsis3/name_of_your_Allas_bucket/name_of_your_input_raster_file.tif')
input_data = open_raster.read()

# Reading vector file directly from Allas using geopandas

vector_file = gpd.read_file('/vsis3/name_of_your_Allas_bucket/name_of_your_input_vector_file.gpkg')

# Setting the end point for Allas for the client
client = boto3.client('s3', endpoint_url='https://a3s.fi')

# List all buckets under own account and project
response = client.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])

# List all objects within a bucket
bucketname = 'name_of_your_Allas_bucket'
response = client.list_objects_v2(Bucket=bucketname)
for object in response['Contents']:
    if object['Key'].endswith('.tif'):
        tif_file_path = f'/vsis3/{bucketname}/{object['Key']}'
        print(tif_file_path)
        #these files can then be opened as seen above

