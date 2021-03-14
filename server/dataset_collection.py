#!/usr/bin/bash python3
# -*- coding: utf-8 -*-

from api.imdb_api import IMDB_MOVIE_LIST, IMDB_MOVIE, REST
import time
import pandas as pd
import json

def get_csv_data():
    return pd.read_csv('./title_list.csv')

def save_datafile( file_index, dictionary ):
    with open('./data/dataset_' + str(file_index) + '.json', 'w') as f:
        json.dump(dictionary, f, indent=4)

def run_dataset_creator():
    print('---title_data_collector---');
    movieList = get_csv_data()
    titleList = movieList['imdb_title_id'].tolist()

    dataset = []
    count = 1
    file_index = 0
    if len(titleList) > 0:
        for title in titleList:
            print('--collecting--' +  title + '::' + str(count) )
            try:
            	movie = IMDB_MOVIE(title)
            	data = movie.parse()
            except Exception as ex:
            	print('ERROR', ex)
            finally:
            	dataset.append(data)
            
            time.sleep(0.00001)
            count += 1
            
            if count%1000 == 0:
                # save dataset 
                save_datafile( file_index, dataset )
                dataset = []
                file_index += 1
                time.sleep(0.001)

if __name__ == '__main__':
    print('data')
    run_dataset_creator()
