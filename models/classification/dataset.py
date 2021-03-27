#!/usr/bin/bash python3
# -*- coding: utf-8 -*-<Paste>

"""
Read all data files and merge them to a panda dataframe
"""

import os
import json
import pandas as pd
from pandas import json_normalize

def get_dataset_list( dir_name ):
	file_list = []
	for file in os.listdir( dir_name ):
		if file.endswith(".json"):
			file_list.append( os.path.join( dir_name , file) )
	return file_list

def get_file_data( file_dir ):
    with open( file_dir ) as data_file:
        return json.load( data_file )

def get_dataframe( dir_name ):
	dataframes = []
	file_list = get_dataset_list( dir_name )
	for file in file_list:
		data = get_file_data( file )
		df = pd.json_normalize(data)
		dataframes.append( df )

	return pd.concat( dataframes )
